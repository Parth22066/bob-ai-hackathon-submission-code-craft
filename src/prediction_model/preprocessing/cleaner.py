"""
Data cleaning and outlier handling module.
Implements SRS FR-03 (Missing Values), FR-04 (Outlier Detection), and FR-05 (Normalization/Bounds).
"""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from data.schemas import VALUE_BOUNDS

class DataCleaner:
    def __init__(self, bounds: Optional[Dict[str, tuple]] = None):
        self.bounds = bounds or VALUE_BOUNDS

    def clip_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clips physical columns to domain-valid bounds."""
        cleaned = df.copy()
        for col, (min_v, max_v) in self.bounds.items():
            if col in cleaned.columns:
                cleaned[col] = cleaned[col].clip(lower=min_v, upper=max_v)
        return cleaned

    def handle_missing_sensor_data(
        self,
        df: pd.DataFrame,
        group_col: str = "asset_id",
        time_col: str = "timestamp",
        max_ffill_limit: int = 4
    ) -> pd.DataFrame:
        """
        Handles missing values per asset:
        1. Sorts chronologically.
        2. Forward fills up to max_ffill_limit.
        3. Backward fills remaining gaps with asset median.
        """
        cleaned = df.copy()
        cleaned = cleaned.sort_values(by=[group_col, time_col]).reset_index(drop=True)
        
        numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
        
        # Forward fill within each asset group
        cleaned[numeric_cols] = cleaned.groupby(group_col)[numeric_cols].transform(
            lambda g: g.ffill(limit=max_ffill_limit)
        )
        
        # Fallback to group median, then global median
        cleaned[numeric_cols] = cleaned.groupby(group_col)[numeric_cols].transform(
            lambda g: g.fillna(g.median())
        )
        cleaned[numeric_cols] = cleaned[numeric_cols].fillna(cleaned[numeric_cols].median())
        
        return cleaned

    def clean_weather_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans and forward fills weather readings per substation."""
        cleaned = df.copy()
        cleaned = cleaned.sort_values(by=["substation_id", "timestamp"]).reset_index(drop=True)
        numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
        cleaned[numeric_cols] = cleaned.groupby("substation_id")[numeric_cols].transform(
            lambda g: g.ffill(limit=6).fillna(g.median())
        )
        return self.clip_outliers(cleaned)
