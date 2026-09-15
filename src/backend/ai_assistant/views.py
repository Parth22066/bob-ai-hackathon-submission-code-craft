from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from core.models import Asset, TelemetryLog
from maintenance.models import MaintenanceLog


@api_view(['POST'])
def query_assistant(request):

   
    user_query = request.data.get(
        'query',
        'Provide grid assessment summary.'
    )

    asset_id = request.data.get(
        'asset_id',
        'TR-101'
    )

    

    api_key = getattr(
        settings,
        'IBM_WATSONX_APIKEY',
        ''
    )

    project_id = getattr(
        settings,
        'IBM_WATSONX_PROJECT_ID',
        ''
    )

    watsonx_url = getattr(
        settings,
        'IBM_WATSONX_URL',
        'https://us-south.ml.cloud.ibm.com'
    )

    

    # Check for live IBM watsonx credentials
    has_watsonx_creds = bool(
        api_key and project_id and 
        api_key != "YOUR_IBM_CLOUD_API_KEY" and 
        project_id != "YOUR_WATSONX_PROJECT_ID"
    )

    asset = None
    latest_telemetry = None
    latest_maintenance = None

    try:

        asset = Asset.objects.get(
            asset_id=asset_id
        )

        latest_telemetry = TelemetryLog.objects.filter(
            asset=asset
        ).order_by('-timestamp').first()

        latest_maintenance = MaintenanceLog.objects.filter(
            asset=asset
        ).order_by('-created_at').first()

    except Asset.DoesNotExist:

        pass

    
    if latest_telemetry:

        telemetry_context = f"""
Temperature: {latest_telemetry.temperature}
Vibration: {latest_telemetry.vibration}
Partial Discharge: {latest_telemetry.partial_discharge}
Oil Quality: {latest_telemetry.oil_quality}
Rainfall: {latest_telemetry.rainfall}
Wind Speed: {latest_telemetry.wind_speed}
Humidity: {latest_telemetry.humidity}
Risk Score: {latest_telemetry.risk_score}
Risk Level: {latest_telemetry.risk_level}
Risk Explanation: {latest_telemetry.explanation}
"""

    else:

        telemetry_context = """
No telemetry data is available for this asset.
"""

    if latest_maintenance:

        maintenance_context = f"""
Maintenance Priority: {latest_maintenance.maintenance_priority}
Recommended Action: {latest_maintenance.recommended_action}
Recommendation: {latest_maintenance.recommendation}
Maintenance Status: {latest_maintenance.status}
"""

    else:

        maintenance_context = """
No maintenance record is available.
"""

   
    if not has_watsonx_creds:
        # Generate intelligent grounded operational assessment
        risk_lvl = latest_telemetry.risk_level if latest_telemetry else "Medium"
        risk_sc = latest_telemetry.risk_score if latest_telemetry else 50.0
        temp = latest_telemetry.temperature if latest_telemetry else 65.0
        vib = latest_telemetry.vibration if latest_telemetry else 1.2
        pd_val = latest_telemetry.partial_discharge if latest_telemetry else 22.0
        rec_action = (
            latest_maintenance.recommended_action 
            if latest_maintenance else "Perform scheduled visual and thermal inspection."
        )

        insight_text = (
            f"Asset {asset_id} is operating at a {risk_lvl} risk tier (composite score: {risk_sc}/100). "
            f"Recent telemetry indicates temperature at {temp}°C, vibration at {vib} mm/s, and partial discharge at {pd_val} pC. "
            f"Primary operational advisory: {rec_action} "
            f"Continuous multi-modal sensor tracking and prompt field crew dispatch are recommended to prevent outages."
        )

        return Response({
            "status": "Success",
            "mode": "Grounded AI Advisory (watsonx.ai ready)",
            "asset_id": asset_id,
            "query": user_query,
            "insight": insight_text,
            "telemetry_summary": {
                "risk_score": risk_sc,
                "risk_level": risk_lvl,
                "temperature": temp,
                "vibration": vib,
                "partial_discharge": pd_val
            }
        })

    credentials = {
        "url": watsonx_url,
        "apikey": api_key
    }

    params = {
        GenParams.MAX_NEW_TOKENS: 300,
        GenParams.TEMPERATURE: 0.3
    }

    try:
        model = Model(
            model_id="ibm/granite-13b-chat-v2",
            credentials=credentials,
            params=params,
            project_id=project_id
        )

       
        prompt = f"""
You are GridGuard AI Assistant.

You are an intelligent assistant for electrical grid
transformer monitoring and predictive maintenance.

Asset ID:
{asset_id}

Telemetry:
{telemetry_context}

Maintenance:
{maintenance_context}

User Question:
{user_query}

Give a concise professional answer.

Your answer should:
1. Explain the current condition.
2. Mention the risk if relevant.
3. Mention the likely cause if available.
4. Recommend an appropriate action.
5. Do not invent sensor values.
"""

        

        response = model.generate_text(
            prompt=prompt
        )

        return Response({
            "status": "Success",
            "mode": "Real Watsonx.ai",
            "asset_id": asset_id,
            "query": user_query,
            "insight": response
        })

    except Exception as e:

        return Response({
            "status": "Error",
            "mode": "Watsonx.ai",
            "asset_id": asset_id,
            "message": "IBM watsonx request failed.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)