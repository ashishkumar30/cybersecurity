from threat_analyzer.models import Threat
from datetime import datetime, timedelta
from .serializers import ThreatSerializer
import pandas as pd
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
import math


def detect_threats(logs_df):
    """
    Detects potential threats from a given logs DataFrame.

    The function analyzes logs for specific threat patterns such as:
    - Credential stuffing attacks (based on failed login attempts)
    - Privilege escalation (based on specific database queries following failed login attempts)
    - Account takeover (based on login activity from a different IP address and access to restricted files)
    - Data exfiltration (based on frequent access to restricted files within a short timeframe)
    - Insider threat (based on file access outside of business hours)

    Args:
        logs_df (pd.DataFrame): DataFrame containing log data with columns like 'user_id', 'ip_address', 'action',
                                 'file_name', 'database_query', and 'timestamp'.

    Returns:
        List[Threat]: A list of `Threat` objects identified in the logs.
    """
    threats = []
    logs_df["timestamp"] = pd.to_datetime(logs_df["timestamp"])  # Convert timestamps to datetime
    logs_df["database_query"] = logs_df["database_query"].fillna("")  # Handle missing database queries
    logs_df = logs_df.sort_values(by="timestamp")  # Sort logs by timestamp

    # Initialize tracking dictionaries for different threat scenarios
    login_failures = {}
    user_ip_timestamps = {}
    file_access_tracker = {}

    RESTRICTED_FILES = ["/secure/payroll.csv", "/confidential/design.pdf", "/db_dump.sql"]
    BUSINESS_HOURS_START = 5  # 5 AM
    BUSINESS_HOURS_END = 2  # 2 AM (next day)

    # Loop through each log row and analyze potential threats
    for _, row in logs_df.iterrows():
        user, ip, action, file_name, query, timestamp = row[
            ["user_id", "ip_address", "action", "file_name", "database_query", "timestamp"]]

        # Detect login failures
        if action == "login_failed":
            login_failures.setdefault(user, []).append(timestamp)

        # Detect credential stuffing if 3 or more login failures precede a successful login
        if action == "login_success" and user in login_failures and len(login_failures[user]) >= 3:
            threats.append((timestamp, user, ip, action, file_name, "CredentialStuffing", "High"))
            login_failures[user] = []  # Reset after threat detection

        # Detect privilege escalation if a dangerous database query follows login failures
        if action == "database_query" and any(op in query for op in ["INSERT", "DELETE"]):
            if user in login_failures and any(
                    timestamp - fail_time <= timedelta(minutes=5) for fail_time in login_failures[user]):
                threats.append((timestamp, user, ip, action, file_name, "PrivilegeEscalation", "High"))

        # Detect account takeover based on different IP access and restricted file access
        if user in user_ip_timestamps and user_ip_timestamps[user][1] != ip and timestamp - user_ip_timestamps[user][
            0] <= timedelta(minutes=10) and file_name in RESTRICTED_FILES:
            threats.append((timestamp, user, ip, action, file_name, "AccountTakeover", "Critical"))
        user_ip_timestamps[user] = (timestamp, ip)

        # Detect data exfiltration based on multiple file accesses within 30 seconds
        if file_name in RESTRICTED_FILES:
            file_access_tracker.setdefault(user, []).append(timestamp)
            file_access_tracker[user] = [t for t in file_access_tracker[user] if timestamp - t <= timedelta(seconds=30)]
            if len(file_access_tracker[user]) > 3:
                threats.append((timestamp, user, ip, action, file_name, "DataExfiltration", "Critical"))

        # Detect insider threat based on file access during non-business hours
        if action == "file_access" and (timestamp.hour < BUSINESS_HOURS_START or timestamp.hour >= BUSINESS_HOURS_END):
            threats.append((timestamp, user, ip, action, file_name, "InsiderThreat", "Medium"))

    # Convert detected threats into Threat model instances
    return [Threat(timestamp=t[0], user_id=t[1], ip_address=t[2], action=t[3], file_name=t[4], threat_type=t[5],
                   severity=t[6]) for t in threats]


def sanitize_value(value):
    """
    Sanitizes values to ensure no NaN, Infinity, or invalid values are included in the response.

    Args:
        value: The value to sanitize.

    Returns:
        The sanitized value, or None if the value is NaN or Infinity.
    """
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None  # Replace invalid values with None
    return value


class ThreatAnalyzeView(APIView):
    """
    View to analyze logs and detect potential threats.

    Accepts a CSV file containing logs, detects threats using the `detect_threats` function,
    and stores the detected threats in the database. Returns the detected threats in JSON format.
    """

    def post(self, request):
        """
        Handle POST request to analyze the uploaded log file and detect threats.

        Args:
            request: The HTTP request containing the uploaded file.

        Returns:
            Response: A JSON response containing the detected threats and a status message.
        """
        # Retrieve the uploaded file
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        # Read CSV logs into a DataFrame and detect threats
        logs_df = pd.read_csv(file)
        threats = detect_threats(logs_df)

        # Bulk create Threat objects in the database
        Threat.objects.bulk_create(threats)

        # Prepare the threats as a JSON response with unique UUIDs as keys
        threats_json = {
            str(uuid.uuid4()): {
                "timestamp": threat.timestamp.isoformat(),
                "user_id": sanitize_value(threat.user_id),
                "ip_address": sanitize_value(threat.ip_address),
                "action": sanitize_value(threat.action),
                "file_name": sanitize_value(threat.file_name),
                "threat_type": sanitize_value(threat.threat_type),
                "severity": sanitize_value(threat.severity),
            }
            for threat in threats
        }

        # Return the formatted JSON response
        return Response(
            {"message": "Threats detected", "Total no of Threats detected": len(threats_json), "threats": threats_json},
            content_type="application/json")


class ThreatListView(generics.ListAPIView):
    """
    View to list all detected threats.

    This view returns all the `Threat` objects stored in the database.
    """
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer


class ThreatDetailView(generics.RetrieveAPIView):
    """
    View to retrieve the details of a specific threat.

    This view retrieves a specific `Threat` object based on its primary key.
    """
    queryset = Threat.objects.all()
    serializer_class = ThreatSerializer


class ThreatSearchView(generics.ListAPIView):
    """
    View to search for threats based on query parameters.

    This view allows filtering threats by type, user, and time range.
    """
    serializer_class = ThreatSerializer

    def get_queryset(self):
        """
        Filter the queryset based on search parameters.

        Args:
            self.request.query_params: The query parameters for filtering.

        Returns:
            queryset: The filtered list of `Threat` objects.
        """
        queryset = Threat.objects.all()
        threat_type = self.request.query_params.get('type')
        user_id = self.request.query_params.get('user')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        # Apply filters based on query parameters
        if threat_type:
            queryset = queryset.filter(threat_type=threat_type)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_time and end_time:
            queryset = queryset.filter(timestamp__range=[start_time, end_time])

        return queryset
