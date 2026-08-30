import numpy as np
from typing import List, Dict, Any

def calculate_precision_at_k(actual_relevant: List[str], recommended: List[str], k: int = 5) -> float:
    """Calculates Precision@K for a single user."""
    rec_k = recommended[:k]
    if not rec_k:
        return 0.0
    hits = sum(1 for item in rec_k if item in actual_relevant)
    return hits / float(k)

def calculate_recall_at_k(actual_relevant: List[str], recommended: List[str], k: int = 5) -> float:
    """Calculates Recall@K for a single user."""
    if not actual_relevant:
        return 0.0
    rec_k = recommended[:k]
    hits = sum(1 for item in rec_k if item in actual_relevant)
    return hits / float(len(actual_relevant))

def calculate_ndcg_at_k(actual_relevant: List[str], recommended: List[str], k: int = 5) -> float:
    """Calculates Normalized Discounted Cumulative Gain (NDCG@K)."""
    rec_k = recommended[:k]
    dcg = 0.0
    for idx, item in enumerate(rec_k):
        if item in actual_relevant:
            dcg += 1.0 / np.log2(idx + 2)  # rank is idx+1, log2(rank+1) = log2(idx+2)

    idcg = sum(1.0 / np.log2(idx + 2) for idx in range(min(len(actual_relevant), k)))
    if idcg == 0.0:
        return 0.0
    return float(dcg / idcg)

def calculate_mrr(actual_relevant: List[str], recommended: List[str]) -> float:
    """Calculates Mean Reciprocal Rank (MRR)."""
    for idx, item in enumerate(recommended):
        if item in actual_relevant:
            return 1.0 / float(idx + 1)
    return 0.0

def evaluate_system_performance(eval_records: List[Dict[str, Any]], k: int = 5) -> Dict[str, float]:
    """
    Evaluates system ranking metrics across a set of evaluation records.
    Each record contains 'actual_relevant' (ground truth) and 'recommended' (system output).
    """
    precisions = []
    recalls = []
    ndcgs = []
    mrrs = []

    for rec in eval_records:
        rel = rec["actual_relevant"]
        recs = rec["recommended"]
        precisions.append(calculate_precision_at_k(rel, recs, k=k))
        recalls.append(calculate_recall_at_k(rel, recs, k=k))
        ndcgs.append(calculate_ndcg_at_k(rel, recs, k=k))
        mrrs.append(calculate_mrr(rel, recs))

    return {
        f"Precision@{k}": float(np.mean(precisions)) if precisions else 0.0,
        f"Recall@{k}": float(np.mean(recalls)) if recalls else 0.0,
        f"NDCG@{k}": float(np.mean(ndcgs)) if ndcgs else 0.0,
        "MRR": float(np.mean(mrrs)) if mrrs else 0.0,
        "total_evaluations": len(eval_records)
    }
