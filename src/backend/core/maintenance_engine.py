# ============================================================
# MAINTENANCE RECOMMENDATION ENGINE
# ============================================================

def generate_maintenance_recommendation(
    risk_score,
    risk_level,
    reasons
):
    """
    Generates maintenance recommendation based on
    equipment risk.
    """

    risk_score = float(risk_score)

    risk_level = str(risk_level).strip().title()

    if risk_level == "Critical":

        priority = "P1"

        action = "Emergency Maintenance"

        recommendation = (
            "Immediate inspection and emergency maintenance "
            "is required. Isolate the asset if necessary."
        )

        estimated_response = "Within 1 hour"

    elif risk_level == "High":

        priority = "P2"

        action = "Urgent Inspection"

        recommendation = (
            "Schedule urgent inspection and maintenance. "
            "Prepare a response crew and required spare parts."
        )

        estimated_response = "Within 4 hours"

    elif risk_level == "Medium":

        priority = "P3"

        action = "Preventive Maintenance"

        recommendation = (
            "Schedule preventive maintenance and continue "
            "close monitoring of the asset."
        )

        estimated_response = "Within 24 hours"

    else:

        priority = "P4"

        action = "Normal Monitoring"

        recommendation = (
            "Asset is operating within acceptable limits. "
            "Continue normal monitoring."
        )

        estimated_response = "Routine schedule"

    # Make sure reasons is always a list
    if not isinstance(reasons, list):
        reasons = []

    return {
        "maintenance_priority": priority,
        "recommended_action": action,
        "recommendation": recommendation,
        "estimated_response": estimated_response,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": reasons
    }