from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.risk_engine import calculate_risk
from core.grid_impact import calculate_grid_impact
from core.maintenance_engine import generate_maintenance_recommendation
from core.models import Asset, TelemetryLog
from maintenance.models import MaintenanceLog
from .ml_bridge import predict_asset_ml


@api_view(['POST'])
def analyze_risk(request):

    data = request.data

    try:
        asset_id = data.get('asset_id', 'TR-101')

        temperature = float(data.get('temperature', 0))
        vibration = float(data.get('vibration', 0))
        partial_discharge = float(data.get('partial_discharge', 0))
        oil_quality = float(data.get('oil_quality', 100))

        wind_speed = float(data.get('wind_speed', 0))
        rainfall = float(data.get('rainfall', 0))
        humidity = float(data.get('humidity', 0))

        grid_importance = int(data.get('grid_importance', 1))
        critical_customers = int(data.get('critical_customers', 0))
        affected_load_mw = float(data.get('affected_load_mw', 0))

        latitude = float(data.get('latitude', 21.76))
        longitude = float(data.get('longitude', 70.45))

    except (ValueError, TypeError):
        return Response(
            {
                "status": "Error",
                "message": "Invalid input data."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ------------------------------------------------
    # 1. CREATE / GET ASSET
    # ------------------------------------------------

    asset, created = Asset.objects.get_or_create(
        asset_id=asset_id,
        defaults={
            "name": f"Transformer {asset_id}",
            "latitude": latitude,
            "longitude": longitude,
            "grid_importance": grid_importance
        }
    )

    # Existing asset hoy to latest values update kariye
    asset.latitude = latitude
    asset.longitude = longitude
    asset.grid_importance = grid_importance
    asset.save()

    # ------------------------------------------------
    # 2. RISK ANALYSIS (ML Engine + Fallback)
    # ------------------------------------------------

    ml_result = predict_asset_ml(
        asset_id=asset_id,
        telemetry_override={
            "temperature": temperature,
            "vibration": vibration,
            "partial_discharge": partial_discharge,
            "oil_quality": oil_quality,
            "wind_speed": wind_speed,
            "rainfall": rainfall,
        }
    )

    if ml_result:
        ml_risk = ml_result["risk_assessment"]
        score = float(ml_risk["composite_risk_score"])
        level = ml_risk["risk_level"]
        explanation = ml_result["explainability"]["recommended_action"]
        reasons = [
            driver["feature"].replace("_", " ").title()
            for driver in ml_result["explainability"].get("top_risk_drivers", [])[:3]
        ]
        if not reasons:
            reasons = ["Nominal telemetry parameters"]
        risk = {
            "risk_score": score,
            "risk_level": level,
            "reasons": reasons,
            "explanation": explanation,
            "failure_probability": ml_result.get("failure_probability", 0.0),
            "sensor_anomaly": ml_result.get("sensor_anomaly", {})
        }
    else:
        risk = calculate_risk(
            temperature=temperature,
            vibration=vibration,
            partial_discharge=partial_discharge,
            oil_quality=oil_quality,
            wind_speed=wind_speed,
            rainfall=rainfall,
            grid_importance=grid_importance
        )

    # ------------------------------------------------
    # 3. GRID IMPACT
    # ------------------------------------------------

    grid_impact = calculate_grid_impact(
        risk_score=risk["risk_score"],
        grid_importance=grid_importance,
        critical_customers=critical_customers,
        affected_load_mw=affected_load_mw
    )

    # ------------------------------------------------
    # 4. MAINTENANCE RECOMMENDATION
    # ------------------------------------------------

    maintenance = generate_maintenance_recommendation(
        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"],
        reasons=risk["reasons"]
    )

    # ------------------------------------------------
    # 5. SAVE TELEMETRY
    # ------------------------------------------------

    telemetry = TelemetryLog.objects.create(
        asset=asset,

        temperature=temperature,
        vibration=vibration,
        partial_discharge=partial_discharge,
        oil_quality=oil_quality,

        rainfall=rainfall,
        wind_speed=wind_speed,
        humidity=humidity,

        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"],
        explanation=risk["explanation"]
    )

    # ------------------------------------------------
    # 6. SAVE MAINTENANCE
    # ------------------------------------------------

    maintenance_log = MaintenanceLog.objects.create(
        asset=asset,

        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"],

        maintenance_priority=maintenance["maintenance_priority"],
        recommended_action=maintenance["recommended_action"],
        recommendation=maintenance["recommendation"],
        estimated_response=maintenance["estimated_response"],

        status="Pending"
    )

    # ------------------------------------------------
    # 7. COMPLETE RESPONSE
    # ------------------------------------------------

    return Response(
        {
            "status": "Success",

            "assessment": {
                "asset": {
                    "asset_id": asset.asset_id,
                    "name": asset.name,
                    "latitude": asset.latitude,
                    "longitude": asset.longitude,
                    "grid_importance": asset.grid_importance
                },

                "telemetry": {
                    "telemetry_id": telemetry.id,
                    "temperature": temperature,
                    "vibration": vibration,
                    "partial_discharge": partial_discharge,
                    "oil_quality": oil_quality,
                    "rainfall": rainfall,
                    "wind_speed": wind_speed,
                    "humidity": humidity
                },

                "risk": {
                    "risk_score": risk["risk_score"],
                    "risk_level": risk["risk_level"],
                    "reasons": risk["reasons"],
                    "explanation": risk["explanation"]
                },

                "grid_impact": {
                    "grid_impact_score": grid_impact["grid_impact_score"],
                    "grid_impact_severity": grid_impact["grid_impact_severity"],
                    "maintenance_priority": grid_impact["maintenance_priority"],
                    "recommended_action": grid_impact["recommended_action"]
                },

                "maintenance": {
                    "maintenance_id": maintenance_log.id,
                    "maintenance_priority": maintenance["maintenance_priority"],
                    "recommended_action": maintenance["recommended_action"],
                    "recommendation": maintenance["recommendation"],
                    "estimated_response": maintenance["estimated_response"],
                    "status": maintenance_log.status
                },

                "ml_details": ml_result
            },

            "message": "Complete GridGuard assessment generated successfully."
        },
        status=status.HTTP_201_CREATED
    )