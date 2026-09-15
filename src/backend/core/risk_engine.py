def calculate_risk(
    temperature,
    vibration,
    partial_discharge,
    oil_quality,
    wind_speed,
    rainfall,
    grid_importance=1
):
    score = 0
    reasons = []

    # -------------------------
    # SENSOR RISK
    # -------------------------

    if temperature > 80:
        score += 35
        reasons.append("High temperature")

    if vibration > 1.5:
        score += 25
        reasons.append("Abnormal vibration")

    if partial_discharge > 70:
        score += 15
        reasons.append("High partial discharge")

    if oil_quality < 50:
        score += 20
        reasons.append("Deteriorated oil quality")

    # -------------------------
    # WEATHER RISK
    # -------------------------

    if wind_speed > 50:
        score += 10
        reasons.append("High wind speed")

    if rainfall > 40:
        score += 10
        reasons.append("Heavy rainfall")

    # -------------------------
    # GRID IMPORTANCE
    # -------------------------

    if grid_importance >= 5:
        score += 10
        reasons.append("Highly critical grid asset")

    elif grid_importance >= 4:
        score += 5
        reasons.append("Important grid asset")

    # Maximum score = 100
    score = min(score, 100)

    # -------------------------
    # RISK LEVEL
    # -------------------------

    if score >= 70:
        level = "Critical"

    elif score >= 40:
        level = "High"

    elif score >= 20:
        level = "Medium"

    else:
        level = "Low"

    # -------------------------
    # EXPLANATION
    # -------------------------

    if reasons:
        explanation = "Risk raised due to " + ", ".join(reasons) + "."

    else:
        explanation = "Normal operating parameters."

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons,
        "explanation": explanation
    }