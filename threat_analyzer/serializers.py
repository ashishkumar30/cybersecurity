"""
Serializer for the Threat model.

This module defines the ThreatSerializer class, which is responsible for 
converting Threat model instances to JSON format and vice versa.
"""

from rest_framework import serializers
from threat_analyzer.models import Threat

class ThreatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Threat model.

    This serializer is used to convert Threat model instances into JSON format 
    and deserialize JSON data into Threat model instances.

    Meta:
        model (Threat): The model associated with this serializer.
        fields (str): Specifies that all model fields should be included.
    """

    class Meta:
        model = Threat  # Specify the model to serialize
        fields = '__all__'  # Include all fields in serialization
