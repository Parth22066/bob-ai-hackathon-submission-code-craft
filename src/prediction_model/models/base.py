"""
Base model interfaces for GridGuard AI ML subsystem.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

class BasePredictor(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "BasePredictor":
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass

    def save(self, file_path: Path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, file_path)

    @classmethod
    def load(cls, file_path: Path) -> "BasePredictor":
        return joblib.load(file_path)
