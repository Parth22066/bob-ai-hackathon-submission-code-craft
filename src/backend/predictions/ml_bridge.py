"""
Bridge service connecting Django REST Framework with the GridGuard AI ML subsystem.
Provides cached access to GridGuardInferenceEngine and fallback mechanisms.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure prediction_model is on sys.path
PREDICTION_MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "prediction_model"
if str(PREDICTION_MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(PREDICTION_MODEL_DIR))

logger = logging.getLogger(__name__)

_engine = None
_data = None


def get_ml_engine():
    global _engine
    if _engine is None:
        try:
            from inference.engine import GridGuardInferenceEngine
            _engine = GridGuardInferenceEngine()
            logger.info("GridGuard ML Inference Engine successfully loaded.")
        except Exception as e:
            logger.warning(f"Could not load ML Inference Engine: {e}")
            _engine = None
    return _engine


def get_ml_data():
    global _data
    if _data is None:
        try:
            from data.loader import DataLoader
            loader = DataLoader()
            _data = loader.load_all()
            logger.info("GridGuard ML baseline datasets successfully loaded.")
        except Exception as e:
            logger.warning(f"Could not load ML baseline data: {e}")
            _data = None
    return _data


def predict_asset_ml(asset_id: str, telemetry_override: Optional[Dict[str, float]] = None) -> Optional[Dict[str, Any]]:
    """
    Runs live prediction for an asset using the calibrated ML models.
    Supports injecting telemetry overrides for real-time risk assessment.
    """
    engine = get_ml_engine()
    data = get_ml_data()

    if engine is None or data is None:
        return None

    try:
        import pandas as pd

        assets_df = data["assets"]
        sensors_df = data["sensors"]
        weather_df = data["weather"]
        incidents_df = data["incidents"]
        maintenance_df = data["maintenance"]

        # Map asset_id if not present directly in assets_df
        target_id = asset_id
        if target_id not in assets_df["asset_id"].values:
            # Fall back to first matching asset or closest EQ-xxx
            target_id = assets_df["asset_id"].iloc[0]

        # If telemetry override is provided, inject dynamic sensor reading
        if telemetry_override:
            temp = float(telemetry_override.get("temperature", 50.0))
            vib = float(telemetry_override.get("vibration", 1.5))
            pd_val = float(telemetry_override.get("partial_discharge", 25.0))
            oil = float(telemetry_override.get("oil_quality", 85.0))
            wind = float(telemetry_override.get("wind_speed", 15.0))
            rain = float(telemetry_override.get("rainfall", 0.0))

            # Temporary synthetic reading for this inference
            sim_sensor = {
                "reading_id": "SIM-LATEST",
                "asset_id": target_id,
                "timestamp": pd.Timestamp.now(),
                "temperature_c": temp,
                "vibration_mms": vib,
                "partial_discharge_pc": pd_val,
                "oil_quality_index": oil,
                "load_current_a": 110.0,
                "voltage_deviation_pct": 0.5,
            }
            sim_df = pd.DataFrame([sim_sensor])
            sensors_df = pd.concat([sensors_df, sim_df], ignore_index=True)

        prediction = engine.predict_asset(
            asset_id=target_id,
            assets_df=assets_df,
            sensors_df=sensors_df,
            weather_df=weather_df,
            incidents_df=incidents_df,
            maintenance_df=maintenance_df,
        )
        prediction["requested_asset_id"] = asset_id
        return prediction

    except Exception as e:
        logger.error(f"Error executing ML inference for asset {asset_id}: {e}")
        return None


def get_top_ml_at_risk_assets(top_n: int = 5):
    """
    Returns the top N at-risk assets according to the ML subsystem.
    """
    engine = get_ml_engine()
    data = get_ml_data()

    if engine is None or data is None:
        return []

    try:
        results = engine.predict_batch(
            assets_df=data["assets"],
            sensors_df=data["sensors"],
            weather_df=data["weather"],
            incidents_df=data["incidents"],
            maintenance_df=data["maintenance"],
        )
        return results[:top_n]
    except Exception as e:
        logger.error(f"Error running batch ML prediction: {e}")
        return []
