# GridGuard AI — Machine Learning Subsystem

Predictive Maintenance & Power Outage Risk Advisory ML Subsystem built strictly in Python, compliant with **GridGuard AI SRS v1.1**.

---

## Capabilities

1. **Equipment Failure Probability Prediction (FR-08):** Supervised XGBoost classifier with Platt/Isotonic probability calibration (`CalibratedClassifierCV`) to forecast failure probability in a configurable horizon (default: 168 hours / 7 days).
2. **Sensor Anomaly Detection (FR-09):** Unsupervised multivariate Isolation Forest on temperature, vibration, partial discharge, oil quality index, load current, and voltage deviation.
3. **Multi-Factor Asset Risk Scoring (FR-10, Section 6):**
   $$\text{Risk Score} = 100 \times \left( 0.35 \cdot P_{\text{failure}} + 0.20 \cdot S_{\text{anomaly}} + 0.15 \cdot R_{\text{weather}} + 0.15 \cdot R_{\text{hist}} + 0.15 \cdot C_{\text{asset}} \right)$$
   Categorizes assets into `Low`, `Medium`, `High`, and `Critical` risk levels.
4. **Leakage-Free Feature Engineering (FR-07):** Strict point-in-time calculation preventing lookahead leakage.
5. **Time-Aware Model Evaluation:** Purged & Embargoed walk-forward cross validation with horizon embargo.
6. **Model Registry & Reproducibility (FR-24):** Versioned artifact persistence (`failure_model.joblib`, `anomaly_detector.joblib`, `metadata.json`).
7. **Explainable AI & IBM watsonx.ai Grounding (FR-17, FR-18):** Outputs top risk drivers, sensor z-score deviations, and structured factual payloads for LLM grounding.

---

## Directory Layout

```
Prediction Model/
├── config/
│   ├── settings.py           # Configuration parameters, paths, horizon settings
│   └── risk_weights.yaml     # Externalized risk scoring weights (FR-10)
├── data/
│   ├── schemas.py            # Data entity validation contracts & physical bounds
│   ├── loader.py             # Multi-source dataset loader & validator
│   └── synthetic_generator.py# Realistic IEEE standard grid telemetry generator
├── preprocessing/
│   ├── cleaner.py            # Outlier clipping & missing value imputation
│   ├── aligner.py            # Multi-source temporal alignment & resampling
│   └── pipeline.py           # Scikit-learn ColumnTransformer pipeline
├── features/
│   ├── sensor_features.py    # Thermal, vibration RMS, partial discharge, oil decay
│   ├── weather_features.py   # Storm index, wind gust, temperature exposure
│   ├── asset_features.py     # Age, maintenance recency, historical failure rates
│   └── builder.py            # Point-in-time feature matrix & forward labeler
├── models/
│   ├── base.py               # Abstract BasePredictor class
│   ├── anomaly/
│   │   └── isolation_forest.py # Isolation Forest unsupervised anomaly detector
│   └── failure/
│       ├── classifier.py     # XGBoost & Random Forest classifier wrappers
│       └── calibrator.py     # Probability calibration (CalibratedClassifierCV)
├── scoring/
│   └── risk_scorer.py        # Multi-factor asset risk scoring engine (FR-10)
├── evaluation/
│   ├── metrics.py            # PR-AUC, ROC-AUC, Brier score, Cost-weighted loss
│   ├── splitters.py          # Purged & Embargoed Time-Series Cross-Validation
│   └── reporter.py           # Markdown evaluation report generator
├── registry/
│   └── model_registry.py     # Version tracking & model bundle loader/saver
├── explainability/
│   └── explainer.py          # Tree feature attributions & watsonx grounding context
├── inference/
│   ├── schemas.py            # Pydantic schemas consumable by Django & watsonx
│   └── engine.py             # Unified single-asset and batch inference engine
├── artifacts/                # Serialized model bundles and metadata
├── scripts/
│   ├── train.py              # CLI to train, calibrate, evaluate, and save models
│   ├── evaluate.py           # CLI to run purged cross-validation
│   └── predict.py            # CLI for single asset and batch inference
├── tests/                    # 10 unit and integration tests (100% passing)
├── requirements.txt
└── README.md
```

---

## Quickstart & CLI Usage

### 1. Run Unit Tests
```bash
python -m pytest tests/
```

### 2. Generate Benchmark Dataset (if needed)
```bash
python -m data.synthetic_generator
```

### 3. Train and Register Model Bundle
```bash
python scripts/train.py
```

### 4. Run Purged & Embargoed Cross-Validation
```bash
python scripts/evaluate.py
```

### 5. Run Live Inference (Single Asset JSON for Django/watsonx)
```bash
python scripts/predict.py --asset-id EQ-015
```

### 6. Run Batch Inference & Risk Ranking
```bash
python scripts/predict.py --batch
```

---

## Django Integration Example

In your Django backend service or Celery task:

```python
from inference.engine import GridGuardInferenceEngine
from data.loader import DataLoader

# Initialize engine (loads latest registered model bundle)
engine = GridGuardInferenceEngine()

# Load latest telemetry
loader = DataLoader()
data = loader.load_all()

# Predict for single asset
prediction_dict = engine.predict_asset(
    asset_id="EQ-001",
    assets_df=data["assets"],
    sensors_df=data["sensors"],
    weather_df=data["weather"],
    incidents_df=data["incidents"],
    maintenance_df=data["maintenance"]
)

# Access calibrated outputs
failure_prob = prediction_dict["failure_probability"]
risk_score = prediction_dict["risk_assessment"]["composite_risk_score"]
watsonx_context = prediction_dict["explainability"]["grounding_context_for_watsonx"]
```
