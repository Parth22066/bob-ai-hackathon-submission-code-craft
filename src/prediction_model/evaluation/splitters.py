"""
Time-Aware Purged & Embargoed Cross-Validation Splitter.
Prevents lookahead leakage and cross-boundary target window overlap.
"""

from typing import List, Tuple, Generator
import pandas as pd
import numpy as np

class PurgedTimeSplitter:
    def __init__(
        self,
        n_splits: int = 3,
        embargo_hours: int = 168, # Equal to prediction horizon H
        time_column: str = "cutoff_timestamp"
    ):
        self.n_splits = n_splits
        self.embargo_hours = embargo_hours
        self.time_column = time_column

    def split(self, df: pd.DataFrame) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        """
        Yields (train_indices, val_indices) for walk-forward evaluation.
        Enforces embargo of length embargo_hours between train and val.
        """
        timestamps = pd.to_datetime(df[self.time_column])
        unique_times = np.sort(timestamps.unique())
        n_times = len(unique_times)
        
        if n_times < self.n_splits + 1:
            raise ValueError(f"Not enough distinct timestamps ({n_times}) for {self.n_splits} splits.")
            
        embargo_delta = pd.Timedelta(hours=self.embargo_hours)
        split_size = n_times // (self.n_splits + 1)
        
        for i in range(1, self.n_splits + 1):
            train_end_idx = i * split_size
            train_end_time = unique_times[train_end_idx]
            
            val_start_time = train_end_time + embargo_delta
            val_end_idx = min(n_times - 1, (i + 1) * split_size)
            val_end_time = unique_times[val_end_idx]
            
            if val_start_time >= val_end_time:
                continue
                
            train_mask = timestamps <= train_end_time
            val_mask = (timestamps >= val_start_time) & (timestamps <= val_end_time)
            
            train_indices = np.where(train_mask)[0]
            val_indices = np.where(val_mask)[0]
            
            if len(train_indices) > 0 and len(val_indices) > 0:
                yield train_indices, val_indices
