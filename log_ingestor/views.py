"""
Views for log management API.

This module defines API endpoints for managing logs, including retrieving,
creating, searching, and filtering logs based on various criteria.
"""

from rest_framework import generics
from django.db.models import Q
from .models import Log
from .serializers import LogSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all logs and creating new log entries.

    - GET: Retrieve a list of all logs.
    - POST: Create a new log entry.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class LogDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single log entry by its primary key (ID).

    - GET: Retrieve a specific log entry.
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class LogSearchView(APIView):
    """
    API endpoint for searching logs based on various filters.

    - POST: Retrieve logs by filtering based on timestamp, user ID, IP address, action, and file name.

    Request Body (JSON):
    {
        "timestamp": "2025-03-26T14:35:21Z",
        "userId": "user123",
        "ipAddress": "192.168.1.10",
        "action": "fileAccess",
        "fileName": "/secure/payroll.csv"
    }

    Response:
    [
        {
            "id": 1,
            "timestamp": "2025-03-26T14:35:21Z",
            "user_id": "user123",
            "ip_address": "192.168.1.10",
            "action": "fileAccess",
            "file_name": "/secure/payroll.csv",
            "database_query": null
        }
    ]
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to search for logs based on dynamic filters.
        """
        filters = Q()  # Initialize an empty filter
        data = request.data  # Extract request payload

        # Extract optional parameters from the request
        timestamp = data.get("timestamp")
        user_id = data.get("userId")  # Ensure field name matches the model
        ip_address = data.get("ipAddress")
        action = data.get("action")
        file_name = data.get("fileName")

        # Apply filters dynamically if parameters are provided
        if timestamp:
            filters &= Q(timestamp__gte=timestamp)  # Filter logs from given timestamp onwards
        if user_id:
            filters &= Q(user_id=user_id)
        if ip_address:
            filters &= Q(ip_address=ip_address)
        if action:
            filters &= Q(action=action)
        if file_name:
            filters &= Q(file_name=file_name)

        # Query logs with applied filters
        logs = Log.objects.filter(filters)
        serializer = LogSerializer(logs, many=True)

        return Response(
            {"status_message": "success", "status_code": 200, "data": serializer.data},
            status=status.HTTP_200_OK
        )
