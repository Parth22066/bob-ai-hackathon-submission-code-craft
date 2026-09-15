"""
Evaluation reporting utility.
Outputs structured markdown reports and logs for evaluation runs.
"""

from typing import Dict, Any
import json
from pathlib import Path

def generate_evaluation_report(metrics: Dict[str, Any], output_path: Path = None) -> str:
    """Formats metrics dictionary into a readable markdown evaluation report."""
    op = metrics.get("operational_metrics", {})
    cm = op.get("confusion_matrix", {})
    
    report = f"""# GridGuard AI Model Evaluation Report
**Timestamp:** {Path().resolve().name}
**Primary Metric (PR-AUC):** {metrics.get('pr_auc')}
**ROC-AUC:** {metrics.get('roc_auc')}
**Brier Score (Calibration):** {metrics.get('brier_score')}
**Recall @ Precision >= 0.70:** {metrics.get('recall_at_precision_70')}

---

## Operational Performance (Decision Threshold: {op.get('threshold_used')})
- **Precision:** {op.get('precision')}
- **Recall:** {op.get('recall')}
- **F1 Score:** {op.get('f1')}
- **Optimal F1 Possible:** {metrics.get('optimal_f1')} (at threshold {metrics.get('optimal_threshold')})

### Confusion Matrix
| Metric | Count |
| :--- | :--- |
| **True Negatives (TN)** | {cm.get('true_negatives')} |
| **False Positives (FP)** | {cm.get('false_positives')} |
| **False Negatives (FN)** | {cm.get('false_negatives')} |
| **True Positives (TP)** | {cm.get('true_positives')} |

### Financial Impact
- **Total Estimated Operational Cost:** ${op.get('total_operational_cost', 0):,.2f}
"""
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
            
    return report
