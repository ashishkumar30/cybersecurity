"""
App configuration for the Threat Analyzer application.

This module defines the ThreatAnalyzerConfig class, which sets up the
Django application configuration for threat analysis.
"""

from django.apps import AppConfig


class ThreatAnalyzerConfig(AppConfig):
    """
    Configuration class for the Threat Analyzer app.

    Attributes:
        default_auto_field (str): Specifies the default auto-incrementing field type.
        name (str): Name of the application registered in Django settings.
    """

    default_auto_field = 'django.db.models.BigAutoField'  # Default primary key type
    name = 'threat_analyzer'  # Name of the Django app
