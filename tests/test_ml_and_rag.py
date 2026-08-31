import numpy as np
from app.ml.ranking_model import LearningToRankModel
from app.rag.knowledge_base import query_knowledge_base

def test_ml_ltr_model():
    ltr = LearningToRankModel(model_type="random_forest")
    assert not ltr.is_trained

    X = np.random.rand(10, 5)
    y = np.random.randint(0, 2, size=10)

    res = ltr.train(X, y)
    assert res["status"] == "success"
    assert ltr.is_trained

    score = ltr.predict_rank_score({"academic_score": 0.8, "interest_score": 0.7, "aptitude_score": 0.6, "preference_score": 0.5, "feasibility_score": 0.9})
    assert 0.0 <= score <= 1.0

def test_rag_knowledge_base_query():
    res = query_knowledge_base("bourses MESRI")
    assert res["matched_documents_count"] > 0
    assert len(res["documents"]) > 0
    assert "disclaimer" in res
