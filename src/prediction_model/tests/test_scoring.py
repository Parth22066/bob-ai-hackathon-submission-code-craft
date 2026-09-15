"""
Tests for multi-factor risk scoring engine (SRS FR-10).
"""

import pytest
from scoring.risk_scorer import AssetRiskScorer

def test_risk_scorer_critical_level():
    scorer = AssetRiskScorer()
    res = scorer.compute_risk(
        failure_probability=0.90,
        anomaly_severity=0.85,
        weather_risk=0.80,
        historical_risk=0.75,
        asset_criticality=1.0
    )
    assert res["risk_level"] == "Critical"
    assert res["composite_risk_score"] >= 85.0

def test_risk_scorer_low_level():
    scorer = AssetRiskScorer()
    res = scorer.compute_risk(
        failure_probability=0.05,
        anomaly_severity=0.05,
        weather_risk=0.10,
        historical_risk=0.05,
        asset_criticality=0.25
    )
    assert res["risk_level"] == "Low"
    assert res["composite_risk_score"] < 35.0

def test_risk_scorer_component_sum():
    scorer = AssetRiskScorer()
    res = scorer.compute_risk(
        failure_probability=0.50,
        anomaly_severity=0.40,
        weather_risk=0.30,
        historical_risk=0.20,
        asset_criticality=0.50
    )
    factors = res["contributing_factors"]
    expected_sum = (
        factors["failure_probability_component"] +
        factors["sensor_anomaly_component"] +
        factors["weather_risk_component"] +
        factors["historical_incident_component"] +
        factors["asset_criticality_component"]
    )
    assert abs(res["composite_risk_score"] - round(expected_sum, 1)) <= 0.2
