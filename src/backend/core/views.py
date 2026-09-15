
import requests
from django.conf import settings
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Asset, TelemetryLog
from .risk_engine import calculate_risk

from maintenance.models import MaintenanceLog





@api_view(['POST'])
def ingest_telemetry(request):
    data = request.data

    asset_id = data.get('asset_id', 'TR-101')
    city = data.get('city', '')

    try:
        asset, created = Asset.objects.get_or_create(
            asset_id=asset_id,
            defaults={
                'name': f"Transformer {asset_id}",
                'latitude': float(data.get('latitude', 21.76)),
                'longitude': float(data.get('longitude', 70.45)),
                'grid_importance': int(data.get('grid_importance', 3))
            }
        )

        temperature = float(data.get('temperature', 0))
        vibration = float(data.get('vibration', 0))
        partial_discharge = float(data.get('partial_discharge', 0))
        oil_quality = float(data.get('oil_quality', 100))
        wind_speed = float(data.get('wind_speed', 0))
        rainfall = float(data.get('rainfall', 0))
        humidity = float(data.get('humidity', 50))

        # --------------------------------------------------------
        # Live Weather Integration
        # --------------------------------------------------------
        weather_used = False
        weather_data = None

        if city:
            api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')

            if api_key:
                try:
                    weather_url = (
                        'https://api.openweathermap.org/data/2.5/weather'
                    )

                    weather_response = requests.get(
                        weather_url,
                        params={
                            'q': city,
                            'appid': api_key,
                            'units': 'metric'
                        },
                        timeout=5
                    )

                    weather_json = weather_response.json()

                    if weather_response.status_code == 200:
                        wind_speed = float(
                            weather_json.get('wind', {}).get(
                                'speed', wind_speed
                            )
                        )

                        rainfall = float(
                            weather_json.get('rain', {}).get(
                                '1h', rainfall
                            )
                        )

                        humidity = float(
                            weather_json.get('main', {}).get(
                                'humidity', humidity
                            )
                        )

                        weather_used = True

                        weather_data = {
                            "city": weather_json.get('name'),
                            "temperature": weather_json.get(
                                'main', {}
                            ).get('temp'),
                            "humidity": humidity,
                            "wind_speed": wind_speed,
                            "rainfall": rainfall,
                            "condition": weather_json.get(
                                'weather', [{}]
                            )[0].get('description', '')
                        }

                except Exception:
                    pass

    except (ValueError, TypeError):
        return Response(
            {
                "status": "Error",
                "message": "Invalid sensor or weather data."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    risk = calculate_risk(
        temperature=temperature,
        vibration=vibration,
        partial_discharge=partial_discharge,
        oil_quality=oil_quality,
        wind_speed=wind_speed,
        rainfall=rainfall,
        grid_importance=asset.grid_importance
    )

    score = risk["risk_score"]
    level = risk["risk_level"]
    reasons = risk["reasons"]
    explanation = risk["explanation"]

    log = TelemetryLog.objects.create(
        asset=asset,
        temperature=temperature,
        vibration=vibration,
        partial_discharge=partial_discharge,
        oil_quality=oil_quality,
        rainfall=rainfall,
        wind_speed=wind_speed,
        humidity=humidity,
        risk_score=score,
        risk_level=level,
        explanation=explanation
    )

    return Response(
        {
            "status": "Success",

            "asset": {
                "asset_id": asset.asset_id,
                "name": asset.name,
                "latitude": asset.latitude,
                "longitude": asset.longitude,
                "grid_importance": asset.grid_importance
            },

            "risk": {
                "risk_score": score,
                "risk_level": level,
                "reasons": reasons,
                "explanation": explanation
            },

            "weather": {
                "used": weather_used,
                "data": weather_data
            },

            "telemetry_id": log.id
        },
        status=status.HTTP_201_CREATED
    )



@api_view(['GET'])
def dashboard_overview(request):

    

    critical_count = TelemetryLog.objects.filter(
        risk_level="Critical"
    ).count()

    high_count = TelemetryLog.objects.filter(
        risk_level="High"
    ).count()

    medium_count = TelemetryLog.objects.filter(
        risk_level="Medium"
    ).count()

    low_count = TelemetryLog.objects.filter(
        risk_level="Low"
    ).count()

    

    if critical_count > 0:
        overall_grid_risk = "CRITICAL"

    elif high_count > 0:
        overall_grid_risk = "HIGH"

    elif medium_count > 0:
        overall_grid_risk = "MEDIUM"

    else:
        overall_grid_risk = "LOW"

    

    pending_maintenance = MaintenanceLog.objects.filter(
        status="Pending"
    ).count()

    in_progress_maintenance = MaintenanceLog.objects.filter(
        status="In Progress"
    ).count()

    completed_maintenance = MaintenanceLog.objects.filter(
        status="Completed"
    ).count()

    cancelled_maintenance = MaintenanceLog.objects.filter(
        status="Cancelled"
    ).count()

    
    p1_count = MaintenanceLog.objects.filter(
        maintenance_priority="P1"
    ).count()

    p2_count = MaintenanceLog.objects.filter(
        maintenance_priority="P2"
    ).count()

    p3_count = MaintenanceLog.objects.filter(
        maintenance_priority="P3"
    ).count()

    p4_count = MaintenanceLog.objects.filter(
        maintenance_priority="P4"
    ).count()

    

    recent_logs = MaintenanceLog.objects.select_related(
        'asset'
    ).order_by('-created_at')[:5]

    recent_maintenance = []

    for log in recent_logs:

        recent_maintenance.append({
            "maintenance_id": log.id,
            "asset_id": log.asset.asset_id,
            "asset_name": log.asset.name,
            "risk_score": log.risk_score,
            "risk_level": log.risk_level,
            "maintenance_priority": log.maintenance_priority,
            "recommended_action": log.recommended_action,
            "status": log.status,
            "created_at": log.created_at
        })

   
    return Response(
        {
            "overall_grid_risk": overall_grid_risk,

            "risk_summary": {
                "critical_assets": critical_count,
                "high_risk_assets": high_count,
                "medium_risk_assets": medium_count,
                "low_risk_assets": low_count
            },

            "maintenance_summary": {
                "pending": pending_maintenance,
                "in_progress": in_progress_maintenance,
                "completed": completed_maintenance,
                "cancelled": cancelled_maintenance,
                "total": (
                    pending_maintenance
                    + in_progress_maintenance
                    + completed_maintenance
                    + cancelled_maintenance
                )
            },

            "maintenance_priority": {
                "P1": p1_count,
                "P2": p2_count,
                "P3": p3_count,
                "P4": p4_count
            },

            "recent_maintenance": recent_maintenance,

            "status": "System Operational"
        }
    )


@api_view(['GET'])
def asset_risk_ranking(request):

    assets = Asset.objects.all()

    ranking = []

    for asset in assets:

        # Asset ni latest telemetry
        latest_log = TelemetryLog.objects.filter(
            asset=asset
        ).order_by('-timestamp').first()

        # Jo telemetry available na hoy
        if not latest_log:
            continue

        # Risk level ne numeric priority
        risk_priority = {
            "Critical": 4,
            "High": 3,
            "Medium": 2,
            "Low": 1
        }

        priority = risk_priority.get(
            latest_log.risk_level,
            0
        )

        ranking.append({
            "asset_id": asset.asset_id,
            "asset_name": asset.name,
            "latitude": asset.latitude,
            "longitude": asset.longitude,
            "grid_importance": asset.grid_importance,

            "risk_score": latest_log.risk_score,
            "risk_level": latest_log.risk_level,

            "explanation": latest_log.explanation,

            "last_updated": latest_log.timestamp,

            "priority": priority
        })

    

    ranking.sort(
        key=lambda x: (
            x["priority"],
            x["risk_score"]
        ),
        reverse=True
    )

    
    for item in ranking:
        item.pop("priority", None)

    return Response({
        "status": "Success",
        "total_assets": len(ranking),
        "ranking": ranking
    })
    
   

@api_view(['GET'])
def asset_details(request, asset_id):

    try:
        asset = Asset.objects.get(asset_id=asset_id)

    except Asset.DoesNotExist:
        return Response(
            {
                "status": "Error",
                "message": "Asset not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    
    latest_log = TelemetryLog.objects.filter(
        asset=asset
    ).order_by('-timestamp').first()

    

    latest_maintenance = MaintenanceLog.objects.filter(
        asset=asset
    ).order_by('-created_at').first()

    

    response_data = {
        "status": "Success",

        "asset": {
            "asset_id": asset.asset_id,
            "name": asset.name,
            "latitude": asset.latitude,
            "longitude": asset.longitude,
            "grid_importance": asset.grid_importance
        }
    }

    

    if latest_log:

        response_data["telemetry"] = {
            "telemetry_id": latest_log.id,
            "temperature": latest_log.temperature,
            "vibration": latest_log.vibration,
            "partial_discharge": latest_log.partial_discharge,
            "oil_quality": latest_log.oil_quality,
            "rainfall": latest_log.rainfall,
            "wind_speed": latest_log.wind_speed,
            "humidity": latest_log.humidity,
            "timestamp": latest_log.timestamp
        }

        response_data["risk"] = {
            "risk_score": latest_log.risk_score,
            "risk_level": latest_log.risk_level,
            "explanation": latest_log.explanation
        }

    else:

        response_data["telemetry"] = None
        response_data["risk"] = None

    

    if latest_maintenance:

        response_data["maintenance"] = {
            "maintenance_id": latest_maintenance.id,
            "priority": latest_maintenance.maintenance_priority,
            "recommended_action": latest_maintenance.recommended_action,
            "recommendation": latest_maintenance.recommendation,
            "estimated_response": latest_maintenance.estimated_response,
            "status": latest_maintenance.status,
            "created_at": latest_maintenance.created_at
        }

    else:

        response_data["maintenance"] = None

    return Response(response_data)