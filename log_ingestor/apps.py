"""
Django application configuration for the 'log_ingestor' app.

This module defines the configuration settings for the 'log_ingestor' application.
It specifies the default primary key field type and the application name.
"""

from django.apps import AppConfig


class LogIngestorConfig(AppConfig):
    """
    Configuration class for the 'log_ingestor' Django application.

    This class is responsible for setting up the application-specific configurations
    such as the default primary key field type.
    """

    # Sets the default auto field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Specifies the name of the application
    name = 'log_ingestor'
