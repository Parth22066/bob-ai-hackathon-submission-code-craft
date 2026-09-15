from django.urls import path
from .views import (
    maintenance_history,
    update_maintenance_status
)

urlpatterns = [
    path(
        'history/',
        maintenance_history,
        name='maintenance_history'
    ),

    path(
        '<int:maintenance_id>/status/',
        update_maintenance_status,
        name='update_maintenance_status'
    ),
]