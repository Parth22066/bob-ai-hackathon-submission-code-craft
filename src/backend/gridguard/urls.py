from django.contrib import admin
from django.urls import path, include

from predictions.views import analyze_risk
from ai_assistant.views import query_assistant
from core.views import dashboard_overview


urlpatterns = [
    path('', dashboard_overview, name='home'),

    path('admin/', admin.site.urls),

    path(
        'api/risk/analyze/',
        analyze_risk,
        name='analyze_risk'
    ),

    path(
        'api/ai/assistant/',
        query_assistant,
        name='query_assistant'
    ),

    path(
        'api/weather/',
        include('weather.urls')
    ),

    path(
        'api/maintenance/',
        include('maintenance.urls')
    ),

    path(
        'api/',
        include('core.urls')
    ),
]