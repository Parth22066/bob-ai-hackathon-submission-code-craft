"""
Inference CLI script for GridGuard AI ML subsystem.
Demonstrates live prediction generation for Django and watsonx.ai integration.
"""

import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.loader import DataLoader
from inference.engine import GridGuardInferenceEngine
from inference.schemas import AssetPredictionOutput

def main():
    parser = argparse.ArgumentParser(description="GridGuard AI Prediction Service")
    parser.add_argument("--asset-id", type=str, default=None, help="Asset ID to score (e.g. EQ-001)")
    parser.add_argument("--batch", action="store_true", help="Score all assets and output ranked ranking list")
    parser.add_argument("--version", type=str, default=None, help="Model version to use")
    args = parser.parse_args()

    loader = DataLoader()
    data = loader.load_all()

    engine = GridGuardInferenceEngine(model_version=args.version)

    if args.batch:
        results = engine.predict_batch(
            data["assets"], data["sensors"], data["weather"],
            data["incidents"], data["maintenance"]
        )
        print(f"Scored {len(results)} assets. Top 5 at-risk assets:")
        for res in results[:5]:
            r_info = res["risk_assessment"]
            print(f"  Asset: {res['asset_id']:<8} | Risk: {r_info['risk_level']:<8} | Score: {r_info['composite_risk_score']:<5} | P(Fail): {res['failure_probability']:.2f}")
    else:
        target_id = args.asset_id or data["assets"]["asset_id"].iloc[0]
        prediction = engine.predict_asset(
            target_id, data["assets"], data["sensors"], data["weather"],
            data["incidents"], data["maintenance"]
        )
        # Validate through Pydantic Contract
        validated = AssetPredictionOutput(**prediction)
        print(json.dumps(validated.model_dump(), indent=2))

if __name__ == "__main__":
    main()
