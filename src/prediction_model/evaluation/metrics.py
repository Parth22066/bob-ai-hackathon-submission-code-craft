"""
Evaluation metrics for predictive maintenance under severe class imbalance.
Computes PR-AUC, ROC-AUC, Brier score, Recall@Precision, and cost-weighted loss.
"""

from typing import Dict, Any, Tuple
import numpy as np
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    brier_score_loss,
    precision_recall_curve,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)

def evaluate_predictions(
    y_true: np.ndarray,
    y_probas: np.ndarray,
    operational_threshold: float = 0.40,
    cost_fn: float = 50000.0, # Cost of unplanned catastrophic outage
    cost_fp: float = 1500.0   # Cost of preventive field inspection
) -> Dict[str, Any]:
    """
    Computes rigorous evaluation metrics tailored to predictive maintenance.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_probas = np.asarray(y_probas, dtype=float)
    
    # 1. Ranking & Calibration Metrics
    has_positives = (y_true == 1).sum() > 0
    has_negatives = (y_true == 0).sum() > 0
    
    pr_auc = float(average_precision_score(y_true, y_probas)) if has_positives else 0.0
    roc_auc = float(roc_auc_score(y_true, y_probas)) if (has_positives and has_negatives) else 0.5
    brier_score = float(brier_score_loss(y_true, y_probas))
    
    # 2. Precision-Recall Curve & Optimal Threshold
    if has_positives and has_negatives:
        precisions, recalls, thresholds = precision_recall_curve(y_true, y_probas)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
        best_idx = np.argmax(f1_scores)
        optimal_threshold = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5
        best_f1 = float(f1_scores[best_idx])
        
        # Recall at target precision >= 0.70
        high_p_mask = precisions >= 0.70
        recall_at_p70 = float(np.max(recalls[high_p_mask])) if np.any(high_p_mask) else 0.0
    else:
        optimal_threshold = operational_threshold
        best_f1 = 0.0
        recall_at_p70 = 0.0
        
    # 3. Performance at Operational Threshold
    y_pred_op = (y_probas >= operational_threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred_op, labels=[0, 1]).ravel()
    
    prec_op = float(precision_score(y_true, y_pred_op, zero_division=0))
    rec_op = float(recall_score(y_true, y_pred_op, zero_division=0))
    f1_op = float(f1_score(y_true, y_pred_op, zero_division=0))
    
    total_cost = float(fn * cost_fn + fp * cost_fp)
    
    return {
        "pr_auc": round(pr_auc, 4),
        "roc_auc": round(roc_auc, 4),
        "brier_score": round(brier_score, 4),
        "recall_at_precision_70": round(recall_at_p70, 4),
        "optimal_threshold": round(optimal_threshold, 4),
        "optimal_f1": round(best_f1, 4),
        "operational_metrics": {
            "threshold_used": operational_threshold,
            "precision": round(prec_op, 4),
            "recall": round(rec_op, 4),
            "f1": round(f1_op, 4),
            "confusion_matrix": {
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp)
            },
            "total_operational_cost": total_cost
        }
    }
