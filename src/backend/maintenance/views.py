from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MaintenanceLog


@api_view(['GET'])
def maintenance_history(request):
    logs = MaintenanceLog.objects.select_related(
        'asset'
    ).order_by('-created_at')

    history = []

    for log in logs:
        history.append({
            "maintenance_id": log.id,
            "asset_id": log.asset.asset_id,
            "asset_name": log.asset.name,
            "risk_score": log.risk_score,
            "risk_level": log.risk_level,
            "maintenance_priority": log.maintenance_priority,
            "recommended_action": log.recommended_action,
            "recommendation": log.recommendation,
            "estimated_response": log.estimated_response,
            "status": log.status,
            "created_at": log.created_at
        })

    return Response({
        "status": "Success",
        "total_records": len(history),
        "maintenance_history": history
    })


@api_view(['PATCH'])
def update_maintenance_status(request, maintenance_id):

    try:
        maintenance = MaintenanceLog.objects.get(
            id=maintenance_id
        )
    except MaintenanceLog.DoesNotExist:
        return Response(
            {
                "status": "Error",
                "message": "Maintenance record not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    new_status = request.data.get("status")

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Completed",
        "Cancelled"
    ]

    if new_status not in allowed_statuses:
        return Response(
            {
                "status": "Error",
                "message": "Invalid status.",
                "allowed_statuses": allowed_statuses
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    maintenance.status = new_status
    maintenance.save()

    return Response({
        "status": "Success",
        "message": "Maintenance status updated successfully.",
        "maintenance_id": maintenance.id,
        "asset_id": maintenance.asset.asset_id,
        "maintenance_status": maintenance.status
    })
    