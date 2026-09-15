"""
Training and model registration script for GridGuard AI ML subsystem.
Executes end-to-end training, probability calibration, evaluation, and serialization.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np

from config.settings import DEFAULT_CONFIG
from data.loader import DataLoader
from features.builder import FeatureBuilder, NUMERICAL_FEATURE_NAMES, CATEGORICAL_FEATURE_NAMES
from models.anomaly.isolation_forest import SensorAnomalyDetector
from models.failure.classifier import EquipmentFailureClassifier
from models.failure.calibrator import CalibratedFailureModel
from evaluation.metrics import evaluate_predictions
from evaluation.reporter import generate_evaluation_report
from registry.model_registry import ModelRegistry

def run_training():
    print("=" * 60)
    print("  GRIDGUARD AI: MODEL TRAINING & CALIBRATION PIPELINE")
    print("=" * 60)
    
    # 1. Ingestion & Validation
    print("\n[Step 1/6] Loading and validating multi-source grid datasets...")
    loader = DataLoader()
    data = loader.load_all()
    print(f"  Loaded {len(data['assets'])} assets, {len(data['sensors'])} sensor readings, {len(data['incidents'])} incidents.")
    
    # 2. Train Sensor Anomaly Detector (Unsupervised Isolation Forest)
    print("\n[Step 2/6] Training Unsupervised Sensor Anomaly Detector (Isolation Forest)...")
    anomaly_detector = SensorAnomalyDetector(
        contamination=DEFAULT_CONFIG.anomaly_contamination,
        n_estimators=DEFAULT_CONFIG.anomaly_n_estimators,
        random_state=DEFAULT_CONFIG.random_state
    )
    anomaly_detector.fit(data["sensors"])
    print("  Anomaly detector trained and calibrated with empirical decision boundary.")
    
    # 3. Construct Leak-Free Point-in-Time Training Matrix
    print(f"\n[Step 3/6] Generating point-in-time feature matrix (Horizon: {DEFAULT_CONFIG.prediction_horizon_hours}h, Lead: {DEFAULT_CONFIG.lead_time_hours}h)...")
    feature_builder = FeatureBuilder(DEFAULT_CONFIG)
    dataset = feature_builder.build_training_dataset(
        data["assets"], data["sensors"], data["weather"],
        data["incidents"], data["maintenance"],
        cutoff_interval_hours=24 # 24h cadence across full timeline
    )
    print(f"  Constructed feature matrix: {dataset.shape[0]} observations, {dataset.shape[1]} columns.")
    pos_count = int((dataset["target_failure_next_H"] == 1).sum())
    neg_count = int((dataset["target_failure_next_H"] == 0).sum())
    print(f"  Class balance: Positive failures={pos_count}, Normal={neg_count} (Failure rate: {pos_count/len(dataset):.2%})")
    
    # 4. Chronological Train/Test Split (Time-Aware Holdout)
    print("\n[Step 4/6] Partitioning dataset into chronological Train and Holdout Test splits...")
    cutoffs = np.sort(pd.to_datetime(dataset["cutoff_timestamp"]).unique())
    split_point = cutoffs[int(len(cutoffs) * 0.75)]
    
    train_mask = pd.to_datetime(dataset["cutoff_timestamp"]) <= split_point
    test_mask = pd.to_datetime(dataset["cutoff_timestamp"]) > split_point
    
    train_df = dataset[train_mask].copy()
    test_df = dataset[test_mask].copy()
    
    X_train = train_df[NUMERICAL_FEATURE_NAMES + CATEGORICAL_FEATURE_NAMES]
    y_train = train_df["target_failure_next_H"]
    
    X_test = test_df[NUMERICAL_FEATURE_NAMES + CATEGORICAL_FEATURE_NAMES]
    y_test = test_df["target_failure_next_H"]
    
    print(f"  Train split: {len(X_train)} samples up to {split_point}")
    print(f"  Test split:  {len(X_test)} samples after {split_point}")
    
    # 5. Train Supervised Classifier with Probability Calibration
    print("\n[Step 5/6] Training XGBoost Failure Classifier & Calibrating Posterior Probabilities...")
    base_clf = EquipmentFailureClassifier(
        model_type="xgboost",
        random_state=DEFAULT_CONFIG.random_state
    )
    
    calibrated_model = CalibratedFailureModel(base_classifier=base_clf, method="sigmoid")
    calibrated_model.fit(X_train, y_train)
    
    # Feature importances from base model
    feat_importances = base_clf.get_feature_importances()
    print("  Top 5 Predictive Features:")
    for f, imp in list(feat_importances.items())[:5]:
        print(f"    - {f}: {imp:.4f}")
        
    # 6. Evaluation on Out-of-Time Test Set
    print("\n[Step 6/6] Evaluating model on Holdout Test Split...")
    test_probas = calibrated_model.predict_proba(X_test)
    metrics = evaluate_predictions(
        y_test.values,
        test_probas,
        operational_threshold=DEFAULT_CONFIG.operational_decision_threshold
    )
    
    print(f"  - Test PR-AUC: {metrics['pr_auc']:.4f}")
    print(f"  - Test ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  - Test Brier Score (Calibration): {metrics['brier_score']:.4f}")
    print(f"  - Operational Precision: {metrics['operational_metrics']['precision']:.4f}")
    print(f"  - Operational Recall: {metrics['operational_metrics']['recall']:.4f}")
    print(f"  - Operational F1: {metrics['operational_metrics']['f1']:.4f}")
    
    # 7. Model Registration & Artifact Saving
    registry = ModelRegistry(DEFAULT_CONFIG.artifacts_dir)
    version_name = f"v1.1.0-xgb-calibrated-{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
    
    metadata = {
        "model_version": version_name,
        "prediction_horizon_hours": DEFAULT_CONFIG.prediction_horizon_hours,
        "lead_time_hours": DEFAULT_CONFIG.lead_time_hours,
        "operational_decision_threshold": DEFAULT_CONFIG.operational_decision_threshold,
        "metrics": metrics,
        "feature_importances": feat_importances,
        "risk_weights": DEFAULT_CONFIG.risk_weights
    }
    
    save_path = registry.save_bundle(calibrated_model, anomaly_detector, metadata, version_name)
    report = generate_evaluation_report(metrics, save_path / "evaluation_report.md")
    
    print("\n" + "=" * 60)
    print(f"  MODEL BUNDLE REGISTERED: {version_name}")
    print(f"  Location: {save_path}")
    print("=" * 60)

if __name__ == "__main__":
    run_training()
