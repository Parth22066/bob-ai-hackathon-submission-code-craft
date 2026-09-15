# ============================================================
# GRID IMPACT ANALYSIS
# ============================================================

def calculate_grid_impact(
    risk_score,
    grid_importance,
    critical_customers=0,
    affected_load_mw=0
):
    """
    Calculates how much an asset failure could impact the grid.

    Inputs:
        risk_score          -> Asset failure risk (0-100)
        grid_importance     -> Importance of asset (1-5)
        critical_customers  -> Number of important customers
        affected_load_mw    -> Estimated affected electrical load

    Returns:
        Grid impact score
        Impact severity
        Maintenance priority
        Recommended action
    """

    # --------------------------------------------------------
    # Convert values safely
    # --------------------------------------------------------

    risk_score = float(risk_score)
    grid_importance = int(grid_importance)
    critical_customers = int(critical_customers)
    affected_load_mw = float(affected_load_mw)

    # --------------------------------------------------------
    # Base Impact Score
    # --------------------------------------------------------

    impact_score = 0

    # Asset risk contribution
    impact_score += risk_score * 0.50

    # Grid importance contribution
    importance_score = (grid_importance / 5) * 25
    impact_score += importance_score

    # --------------------------------------------------------
    # Customer Impact
    # --------------------------------------------------------

    if critical_customers >= 10000:
        impact_score += 20

    elif critical_customers >= 5000:
        impact_score += 15

    elif critical_customers >= 1000:
        impact_score += 10

    elif critical_customers >= 100:
        impact_score += 5

    # --------------------------------------------------------
    # Load Impact
    # --------------------------------------------------------

    if affected_load_mw >= 100:
        impact_score += 15

    elif affected_load_mw >= 50:
        impact_score += 10

    elif affected_load_mw >= 20:
        impact_score += 5

    # --------------------------------------------------------
    # Limit Score
    # --------------------------------------------------------

    impact_score = min(round(impact_score, 2), 100)

    # --------------------------------------------------------
    # Impact Severity
    # --------------------------------------------------------

    if impact_score >= 75:
        severity = "CRITICAL"

    elif impact_score >= 50:
        severity = "HIGH"

    elif impact_score >= 25:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # --------------------------------------------------------
    # Maintenance Priority
    # --------------------------------------------------------

    if severity == "CRITICAL":
        priority = "P1"
        recommended_action = (
            "Immediate inspection and emergency maintenance required."
        )

    elif severity == "HIGH":
        priority = "P2"
        recommended_action = (
            "Schedule urgent maintenance and prepare response crew."
        )

    elif severity == "MEDIUM":
        priority = "P3"
        recommended_action = (
            "Schedule preventive maintenance and continue monitoring."
        )

    else:
        priority = "P4"
        recommended_action = (
            "Continue normal monitoring."
        )

    # --------------------------------------------------------
    # Return Result
    # --------------------------------------------------------

    return {
        "grid_impact_score": impact_score,
        "grid_impact_severity": severity,
        "maintenance_priority": priority,
        "recommended_action": recommended_action
    }