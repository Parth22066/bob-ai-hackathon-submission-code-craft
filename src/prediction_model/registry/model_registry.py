"""
Model version tracking and artifact serialization registry.
Implements SRS Section 6 (Model Version Tracking) and NFR-10 (Auditability).
"""

from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path
from datetime import datetime
import json
import joblib

from config.settings import DEFAULT_CONFIG, MLConfig

class ModelRegistry:
    def __init__(self, artifacts_dir: Optional[Path] = None):
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else DEFAULT_CONFIG.artifacts_dir
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def save_bundle(
        self,
        failure_model: Any,
        anomaly_detector: Any,
        metadata: Dict[str, Any],
        version_name: Optional[str] = None
    ) -> Path:
        """
        Saves calibrated failure model, anomaly detector, and metadata bundle.
        """
        if version_name is None:
            ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_name = f"model_{ts_str}"
            
        target_dir = self.artifacts_dir / version_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Save binaries
        joblib.dump(failure_model, target_dir / "failure_model.joblib")
        joblib.dump(anomaly_detector, target_dir / "anomaly_detector.joblib")
        
        # Enrich metadata
        metadata["model_version"] = version_name
        metadata["saved_at"] = datetime.now().isoformat()
        
        with open(target_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
            
        # Update latest pointer
        with open(self.artifacts_dir / "latest_version.txt", "w", encoding="utf-8") as f:
            f.write(version_name)
            
        return target_dir

    def load_bundle(self, version_name: Optional[str] = None) -> Tuple[Any, Any, Dict[str, Any]]:
        """
        Loads model binaries and metadata for inference.
        """
        if version_name is None:
            latest_file = self.artifacts_dir / "latest_version.txt"
            if not latest_file.exists():
                raise FileNotFoundError("No registered models found in registry.")
            with open(latest_file, "r", encoding="utf-8") as f:
                version_name = f.read().strip()
                
        model_dir = self.artifacts_dir / version_name
        if not model_dir.exists():
            raise FileNotFoundError(f"Model version {version_name} not found in {self.artifacts_dir}")
            
        failure_model = joblib.load(model_dir / "failure_model.joblib")
        anomaly_detector = joblib.load(model_dir / "anomaly_detector.joblib")
        
        with open(model_dir / "metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
            
        return failure_model, anomaly_detector, metadata

    def list_versions(self) -> List[Dict[str, Any]]:
        """Lists all registered model versions."""
        versions = []
        for d in self.artifacts_dir.iterdir():
            if d.is_dir() and (d / "metadata.json").exists():
                with open(d / "metadata.json", "r", encoding="utf-8") as f:
                    meta = json.load(f)
                versions.append(meta)
        return sorted(versions, key=lambda x: x.get("saved_at", ""), reverse=True)
