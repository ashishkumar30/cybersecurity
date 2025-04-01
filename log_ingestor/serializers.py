"""
Serializer for the Log model.

This module defines the LogSerializer class, which converts Log model instances 
into JSON format and vice versa for API interactions.
"""

from rest_framework import serializers
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    """
    Serializer for the Log model.

    This serializer automatically converts Log model instances to JSON format
    and handles deserialization of incoming API data.

    Meta Attributes:
        model (Log): Specifies the model to serialize.
        fields (str): Includes all fields from the Log model.
    """

    class Meta:
        model = Log  # Define the model to serialize
        fields = '__all__'  # Include all fields from the Log model
