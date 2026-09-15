from django.db import models

# Create your models here.

from core.models import Asset


class MaintenanceLog(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='maintenance_logs'
    )

    risk_score = models.FloatField(default=0.0)

    risk_level = models.CharField(
        max_length=20,
        default='Low'
    )

    maintenance_priority = models.CharField(
        max_length=10,
        default='P4'
    )

    recommended_action = models.CharField(
        max_length=100
    )

    recommendation = models.TextField()

    estimated_response = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.asset.asset_id} - "
            f"{self.maintenance_priority} - "
            f"{self.status}"
        )