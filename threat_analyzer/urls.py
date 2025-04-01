"""
URL configuration for the Threat Management API.

This module defines the URL patterns for the Threat Management API, including
routes for analyzing, listing, viewing details, and searching threats. The API
views are implemented using Django's class-based views.

URL patterns:
- `api/threats/analyze`: Trigger threat analysis (POST request). Handled by `ThreatAnalyzeView`.
- `api/threats`: List all threats (GET request). Handled by `ThreatAnalyzeView`.
- `api/threats/<int:pk>`: Retrieve detailed information for a specific threat identified by its primary key (GET request). Handled by `ThreatDetailView`.
- `api/threats/search`: Search for threats based on specified parameters (GET request). Handled by `ThreatSearchView`.
"""


from django.urls import path
from .views import ThreatAnalyzeView, ThreatDetailView, ThreatSearchView

# URL configuration for the Threat Management API
#
# This file defines the URL patterns for the Threat Management API endpoints.
# Each endpoint is associated with a view class that handles HTTP requests
# related to threat analysis, listing, detail retrieval, and searching threats.

urlpatterns = [
    # Endpoint to trigger threat analysis (POST request).
    # This will be handled by the ThreatAnalyzeView class.
    path('api/threats/analyze', ThreatAnalyzeView.as_view(), name='threat-analyze'),

    # Endpoint to retrieve a list of all threats (GET request).
    # This will be handled by the ThreatAnalyzeView class.
    path('api/threats', ThreatAnalyzeView.as_view(), name='threat-list'),

    # Endpoint to retrieve details of a specific threat identified by its primary key (pk).
    # This will be handled by the ThreatDetailView class.
    # The <int:pk> part captures the primary key of the threat to fetch.
    path('api/threats/<int:pk>', ThreatDetailView.as_view(), name='threat-detail'),

    # Endpoint to search for threats (GET request).
    # This will be handled by the ThreatSearchView class.
    path('api/threats/search', ThreatSearchView.as_view(), name='threat-search'),
]
