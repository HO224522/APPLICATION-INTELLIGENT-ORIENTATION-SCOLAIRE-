import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

class LearningToRankModel:
    """
    ML ranking model framework supporting version evolution:
    Version 1: Rule-based + Weighted Scoring Engine (Fallback)
    Version 2: ML-trained ranker (Logistic Regression / Random Forest Classifier / Learning to Rank)
    """
    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.is_trained = False
        if model_type == "logistic_regression":
            self.model = LogisticRegression()
        elif model_type == "random_forest":
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def extract_features(self, breakdown: Dict[str, float]) -> np.ndarray:
        """Transforms compatibility breakdown vector into ML feature vector."""
        return np.array([
            breakdown.get("academic_score", 0.0),
            breakdown.get("interest_score", 0.0),
            breakdown.get("aptitude_score", 0.0),
            breakdown.get("preference_score", 0.0),
            breakdown.get("feasibility_score", 0.0)
        ]).reshape(1, -1)

    def train(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Trains model on historical/validated expert decisions dataset.
        X: Feature matrix [n_samples, 5]
        y: Binary target (1 = Accepted/Success, 0 = Rejected/Unsuitable)
        """
        if len(X) == 0:
            return {"status": "error", "message": "Aucune donnée de réentraînement fournie."}

        self.model.fit(X, y)
        self.is_trained = True
        train_acc = float(self.model.score(X, y))
        return {
            "status": "success",
            "model_type": self.model_type,
            "training_samples": len(X),
            "training_accuracy": train_acc
        }

    def predict_rank_score(self, breakdown: Dict[str, float]) -> float:
        """Predicts ranking probability if trained, otherwise returns rule-based global score."""
        if not self.is_trained:
            return breakdown.get("global_score", 0.0)

        feat = self.extract_features(breakdown)
        probs = self.model.predict_proba(feat)
        return float(probs[0][1])  # Probability of class 1 (Accepted/Success)
