from django.urls import path
from .views import get_live_weather

urlpatterns = [
    path('live/', get_live_weather, name='live_weather'),
]