"""
Django models for storing log data.

This module defines the Log model, which captures user activity logs, including
timestamps, user details, IP addresses, actions performed, file access, and database queries.
"""

from django.db import models


class Log(models.Model):
    """
    Model representing user activity logs.

    Attributes:
        id (AutoField): Primary key, auto-incremented.
        timestamp (DateTimeField): Automatically captures the timestamp of the log entry.
        user_id (CharField): Stores the ID of the user performing the action.
        ip_address (GenericIPAddressField): Stores the IP address of the user.
        action (CharField): Describes the action performed by the user.
        file_name (CharField, optional): Name of the accessed file, if applicable.
        database_query (TextField, optional): Stores database queries executed, if applicable.
    """

    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    timestamp = models.DateTimeField(auto_now=True)  # Auto-updates timestamp on each save
    user_id = models.CharField(max_length=100)  # User identifier (could be username or ID)
    ip_address = models.GenericIPAddressField()  # Captures user IP address
    action = models.CharField(max_length=100)  # Description of the action performed
    file_name = models.CharField(max_length=255, null=True, blank=True)  # Optional file name if accessed
    database_query = models.TextField(null=True, blank=True)  # Optional database query executed by the user

    def __str__(self):
        """
        String representation of the Log object.

        Returns:
            str: A formatted string showing the log details.
        """
        return f"[{self.timestamp}] {self.user_id} - {self.action} @ {self.ip_address}"

