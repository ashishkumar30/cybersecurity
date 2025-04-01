"""
Threat model for storing detected security threats.

This module defines the Threat model, which stores information about 
potential security threats detected in system logs.
"""

from django.db import models

class Threat(models.Model):
    """
    Model representing a detected security threat.

    Attributes:
        id (AutoField): Primary key for the threat record.
        timestamp (DateTimeField): Timestamp of when the threat was detected.
        user_id (CharField): ID of the user associated with the activity.
        ip_address (GenericIPAddressField): IP address from which the activity originated.
        action (CharField): The type of action performed (e.g., login, file access).
        file_name (CharField): Name of the file accessed (if applicable).
        threat_type (CharField): Category of the detected threat (e.g., CredentialStuffing, DataExfiltration).
        severity (CharField): Severity level of the threat (e.g., Low, Medium, High).
    """

    id = models.AutoField(primary_key=True)  # Unique ID for each threat
    timestamp = models.DateTimeField()  # When the threat was detected
    user_id = models.CharField(max_length=100)  # Associated user ID
    ip_address = models.GenericIPAddressField()  # Source IP address
    action = models.CharField(max_length=100)  # Type of action performed
    file_name = models.CharField(max_length=255, null=True, blank=True)  # Optional file name
    threat_type = models.CharField(max_length=100)  # Type of detected threat
    severity = models.CharField(max_length=50)  # Threat severity level (Low, Medium, High)

    def __str__(self):
        """
        String representation of a Threat instance.

        Returns:
            str: A readable format of the threat instance.
        """
        return f"[{self.threat_type}] {self.user_id} - {self.severity}"
