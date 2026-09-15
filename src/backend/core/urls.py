from django.urls import path

from . import views

urlpatterns = [

    path(
        'ingest/',
        views.ingest_telemetry,
        name='ingest'
    ),

    path(
        'dashboard/',
        views.dashboard_overview,
        name='dashboard'
    ),

    path(
        'assets/ranking/',
        views.asset_risk_ranking,
        name='asset_risk_ranking'
    ),

    path(
        'assets/<str:asset_id>/details/',
        views.asset_details,
        name='asset_details'
    ),
]