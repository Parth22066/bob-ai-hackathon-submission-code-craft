"""
Evaluation script for Purged & Embargoed Walk-Forward Cross-Validation.
Evaluates model robustness across rolling time periods.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np

from config.settings import DEFAULT_CONFIG
from data.loader import DataLoader
from features.builder import FeatureBuilder, NUMERICAL_FEATURE_NAMES, CATEGORICAL_FEATURE_NAMES
from evaluation.splitters import PurgedTimeSplitter
from evaluation.metrics import evaluate_predictions
from models.failure.classifier import EquipmentFailureClassifier
from models.failure.calibrator import CalibratedFailureModel

def run_cross_validation():
    print("=" * 65)
    print("  GRIDGUARD AI: PURGED & EMBARGOED TIME-SERIES CROSS-VALIDATION")
    print("=" * 65)
    
    loader = DataLoader()
    data = loader.load_all()
    
    feature_builder = FeatureBuilder(DEFAULT_CONFIG)
    dataset = feature_builder.build_training_dataset(
        data["assets"], data["sensors"], data["weather"],
        data["incidents"], data["maintenance"],
        cutoff_interval_hours=24
    )
    
    splitter = PurgedTimeSplitter(
        n_splits=4,
        embargo_hours=DEFAULT_CONFIG.prediction_horizon_hours,
        time_column="cutoff_timestamp"
    )
    
    features = NUMERICAL_FEATURE_NAMES + CATEGORICAL_FEATURE_NAMES
    X = dataset[features]
    y = dataset["target_failure_next_H"]
    
    fold_metrics = []
    
    for fold, (train_idx, val_idx) in enumerate(splitter.split(dataset), start=1):
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
        
        pos_tr = int((y_tr == 1).sum())
        pos_val = int((y_val == 1).sum())
        
        print(f"\n--- Fold {fold} ---")
        print(f"  Train: {len(X_tr)} samples ({pos_tr} positive failures)")
        print(f"  Val:   {len(X_val)} samples ({pos_val} positive failures)")
        
        if pos_tr < 2:
            print("  [Notice] Skipping fold: Initial burn-in period has fewer than 2 observed failures.")
            continue
            
        if pos_val < 1:
            print("  [Notice] Skipping fold: Validation window has 0 failure events.")
            continue
            
        base_clf = EquipmentFailureClassifier(model_type="xgboost", random_state=DEFAULT_CONFIG.random_state)
        calibrated = CalibratedFailureModel(base_classifier=base_clf, method="sigmoid")
        calibrated.fit(X_tr, y_tr)
        
        val_probas = calibrated.predict_proba(X_val)
        m = evaluate_predictions(y_val.values, val_probas, operational_threshold=DEFAULT_CONFIG.operational_decision_threshold)
        fold_metrics.append(m)
        
        print(f"  PR-AUC:    {m['pr_auc']:.4f} | ROC-AUC: {m['roc_auc']:.4f} | Brier: {m['brier_score']:.4f}")
        print(f"  Precision: {m['operational_metrics']['precision']:.4f} | Recall: {m['operational_metrics']['recall']:.4f} | F1: {m['operational_metrics']['f1']:.4f}")
        
    if fold_metrics:
        avg_pr_auc = np.mean([m["pr_auc"] for m in fold_metrics])
        avg_roc_auc = np.mean([m["roc_auc"] for m in fold_metrics])
        avg_brier = np.mean([m["brier_score"] for m in fold_metrics])
        
        print("\n" + "=" * 65)
        print("  CROSS-VALIDATION SUMMARY ACROSS EMBARGOED FOLDS")
        print(f"  Folds Evaluated: {len(fold_metrics)}")
        print(f"  Mean PR-AUC:     {avg_pr_auc:.4f}")
        print(f"  Mean ROC-AUC:    {avg_roc_auc:.4f}")
        print(f"  Mean Brier:      {avg_brier:.4f}")
        print("=" * 65)
    else:
        print("\nNo valid folds with failure observations in both train and validation.")

if __name__ == "__main__":
    run_cross_validation()
