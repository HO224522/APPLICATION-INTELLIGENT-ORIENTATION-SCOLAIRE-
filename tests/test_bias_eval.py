import json
from app.models.schemas import StudentProfile, FieldProfile
from app.evaluation.metrics import evaluate_system_performance
from app.evaluation.bias_audit import audit_recommendation_bias
from app.recommendation.ranking import rank_fields_for_student

def test_bias_and_evaluation_metrics():
    with open("data/synthetic/fields.json") as f:
        fields = [FieldProfile(**item) for item in json.load(f)]
    with open("data/synthetic/students.json") as f:
        students = [StudentProfile(**item) for item in json.load(f)]

    audit = audit_recommendation_bias(students, fields)
    assert audit.total_profiles_audited == 100
    assert isinstance(audit.summary, str)

    eval_records = []
    for s in students[:20]:
        recs = rank_fields_for_student(s, fields, top_k=5)
        rec_ids = [r.field_id for r in recs]
        eval_records.append({
            "actual_relevant": ["FIELD_INFO_01", "FIELD_ELEC_01"],
            "recommended": rec_ids
        })

    metrics = evaluate_system_performance(eval_records, k=5)
    assert "NDCG@5" in metrics
    assert "Precision@5" in metrics
    assert metrics["total_evaluations"] == 20
