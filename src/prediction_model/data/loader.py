"""
Data loading and ingestion layer for GridGuard AI.
Loads tabular entities, parses timestamps, and validates schema constraints.
"""

from pathlib import Path
from typing import Dict, Tuple, Optional
import pandas as pd

from data.schemas import (
    ASSET_COLUMNS,
    SENSOR_COLUMNS,
    WEATHER_COLUMNS,
    INCIDENT_COLUMNS,
    MAINTENANCE_COLUMNS,
    validate_dataframe
)
from config.settings import DEFAULT_CONFIG

class DataLoader:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_CONFIG.data_dir

    def load_assets(self, filename: str = "assets.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Assets file not found at {path}")
        df = pd.read_csv(path)
        df["installation_date"] = pd.to_datetime(df["installation_date"])
        valid, errs = validate_dataframe(df, ASSET_COLUMNS, "Assets")
        if not valid:
            raise ValueError(f"Asset validation failed: {errs}")
        return df

    def load_sensors(self, filename: str = "sensor_readings.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Sensor readings file not found at {path}")
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        valid, errs = validate_dataframe(df, SENSOR_COLUMNS, "SensorReadings")
        if not valid:
            raise ValueError(f"Sensor readings validation failed: {errs}")
        return df

    def load_weather(self, filename: str = "weather_records.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Weather records file not found at {path}")
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        valid, errs = validate_dataframe(df, WEATHER_COLUMNS, "WeatherRecords")
        if not valid:
            raise ValueError(f"Weather validation failed: {errs}")
        return df

    def load_incidents(self, filename: str = "historical_incidents.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Incidents file not found at {path}")
        df = pd.read_csv(path)
        df["start_timestamp"] = pd.to_datetime(df["start_timestamp"])
        df["end_timestamp"] = pd.to_datetime(df["end_timestamp"])
        valid, errs = validate_dataframe(df, INCIDENT_COLUMNS, "Incidents")
        if not valid:
            raise ValueError(f"Incident validation failed: {errs}")
        return df

    def load_maintenance(self, filename: str = "maintenance_records.csv") -> pd.DataFrame:
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Maintenance file not found at {path}")
        df = pd.read_csv(path)
        df["scheduled_date"] = pd.to_datetime(df["scheduled_date"])
        df["completed_date"] = pd.to_datetime(df["completed_date"])
        valid, errs = validate_dataframe(df, MAINTENANCE_COLUMNS, "Maintenance")
        if not valid:
            raise ValueError(f"Maintenance validation failed: {errs}")
        return df

    def load_ml_dataset(self, filename: str = "gridguard_ml_dataset.csv") -> pd.DataFrame:
        """Loads the unified machine learning dataset table."""
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"ML dataset file not found at {path}")
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    def load_all(self) -> Dict[str, pd.DataFrame]:
        return {
            "assets": self.load_assets(),
            "sensors": self.load_sensors(),
            "weather": self.load_weather(),
            "incidents": self.load_incidents(),
            "maintenance": self.load_maintenance()
        }
