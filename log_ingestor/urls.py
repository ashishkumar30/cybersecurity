"""
URL configuration for the log management API.

This module defines the URL patterns for handling log-related operations, 
including retrieving, creating, updating, deleting, and searching logs.
"""

from django.urls import path
from .views import LogListCreateView, LogDetailView, LogSearchView

# Define URL patterns for the log-related API endpoints
urlpatterns = [
    path('api/logs', LogListCreateView.as_view(), name='log-list-create'), #Endpoint for listing all logs and creating new logs
    path('api/logs/<int:pk>', LogDetailView.as_view(), name='log-detail'), #Endpoint for retrieving, updating, or deleting a specific log entry by ID
    path('api/logs/search', LogSearchView.as_view(), name='log-search'),# Endpoint for searching logs based on filters like timestamp, user, or IP address
]
