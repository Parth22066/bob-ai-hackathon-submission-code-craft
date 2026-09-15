from django.db import models

# Create your models here.


class Asset(models.Model):
    asset_id = models.CharField(max_length=50, unique=True) # e.g., TR-101
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    grid_importance = models.IntegerField(default=1) # 1 to 5 scale

    def __str__(self):
        return f"{self.asset_id} - {self.name}"

class TelemetryLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='telemetry')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Sensor Data
    temperature = models.FloatField()
    vibration = models.FloatField()
    partial_discharge = models.FloatField()
    oil_quality = models.FloatField()
    
    # Weather Data
    rainfall = models.FloatField()
    wind_speed = models.FloatField()
    humidity = models.FloatField()

    # Calculated Output (ML / Rule Engine)
    risk_score = models.FloatField(default=0.0)
    risk_level = models.CharField(max_length=20, default='Low') # Low, Medium, High, Critical
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.asset.asset_id} - {self.risk_level} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"