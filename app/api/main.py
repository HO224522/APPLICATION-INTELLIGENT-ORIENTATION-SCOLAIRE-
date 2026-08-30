import json
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Body
from app.models.schemas import (
    StudentProfile, FieldProfile, RecommendationResponse,
    RecommendationItem, FeedbackItem, AuditReport
)
from app.recommendation.ranking import rank_fields_for_student
from app.services.counterfactual import simulate_counterfactual_improvements
from app.services.comparator import compare_fields
from app.services.action_plan import generate_action_plan
from app.services.feedback import record_human_feedback, get_all_feedback
from app.rag.knowledge_base import query_knowledge_base
from app.evaluation.bias_audit import audit_recommendation_bias
from app.evaluation.metrics import evaluate_system_performance

app = FastAPI(
    title="Burkina Faso Educational Guidance AI Engine API",
    description="Engine for school, university, and professional guidance adapted to Burkina Faso.",
    version="1.0.0"
)

# Helper function to load synthetic fields
def _load_fields() -> List[FieldProfile]:
    fields_path = "data/synthetic/fields.json"
    if not os.path.exists(fields_path):
        return []
    with open(fields_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [FieldProfile(**item) for item in data]

# Helper function to load synthetic student profiles
def _load_students() -> List[StudentProfile]:
    students_path = "data/synthetic/students.json"
    if not os.path.exists(students_path):
        return []
    with open(students_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [StudentProfile(**item) for item in data]

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Burkina Faso Educational Guidance AI Engine",
        "documentation": "/docs"
    }

@app.get("/fields", response_model=List[FieldProfile])
def get_fields():
    """Returns catalog of study fields with official metadata."""
    return _load_fields()

@app.get("/fields/{field_id}", response_model=FieldProfile)
def get_field_by_id(field_id: str):
    fields = _load_fields()
    for f in fields:
        if f.field_id == field_id:
            return f
    raise HTTPException(status_code=404, detail="Filière non trouvée.")

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    student_profile: StudentProfile = Body(...),
    top_k: int = Query(5, ge=1, le=20)
):
    """
    Main endpoint: Processes student profile through compatibility engines and returns Top-K ranked fields.
    """
    fields = _load_fields()
    if not fields:
        raise HTTPException(status_code=500, detail="Catalogue des filières indisponible.")

    rankings = rank_fields_for_student(student_profile, fields, top_k=top_k)
    return RecommendationResponse(
        student_id=student_profile.student_id,
        recommendations=rankings
    )

@app.post("/compare")
def compare_selected_fields(
    student_profile: StudentProfile = Body(...),
    field_ids: List[str] = Body(...)
):
    """Side-by-side comparison of selected fields."""
    all_fields = _load_fields()
    selected_fields = [f for f in all_fields if f.field_id in field_ids]
    if not selected_fields:
        raise HTTPException(status_code=400, detail="Aucune filière valide sélectionnée pour la comparaison.")

    return compare_fields(student_profile, selected_fields)

@app.post("/simulate")
def simulate_counterfactual(
    student_profile: StudentProfile = Body(...),
    target_field_id: str = Body(...),
    subject_improvements: Dict[str, float] = Body(...)
):
    """Simulates grade improvements ('What to improve?') and projects compatibility gains."""
    all_fields = _load_fields()
    target = next((f for f in all_fields if f.field_id == target_field_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Filière cible non trouvée.")

    return simulate_counterfactual_improvements(student_profile, target, subject_improvements)

@app.post("/action-plan")
def get_action_plan(
    student_profile: StudentProfile = Body(...),
    target_field_id: str = Body(...)
):
    """Generates structured career action plan and roadmap."""
    all_fields = _load_fields()
    target = next((f for f in all_fields if f.field_id == target_field_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Filière cible non trouvée.")

    return generate_action_plan(student_profile, target)

@app.post("/feedback", response_model=FeedbackItem)
def submit_expert_feedback(
    recommendation_id: str = Body(...),
    expert_id: str = Body(...),
    decision: str = Body(...),
    reason: str = Body(...),
    suggested_field_id: Optional[str] = Body(None)
):
    """Logs human orientation expert feedback (accepted/modified/rejected)."""
    try:
        return record_human_feedback(
            recommendation_id=recommendation_id,
            expert_id=expert_id,
            decision=decision,
            reason=reason,
            suggested_field_id=suggested_field_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/feedback", response_model=List[FeedbackItem])
def list_feedback():
    return get_all_feedback()

@app.post("/rag/query")
def search_knowledge_base(query: str = Query(...)):
    """Queries official institutional verified educational documentation."""
    return query_knowledge_base(query)

@app.get("/audit/bias", response_model=AuditReport)
def run_bias_audit():
    """Runs demographic parity bias audit across synthetic profiles."""
    students = _load_students()
    fields = _load_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'audit non chargées.")
    return audit_recommendation_bias(students, fields)

@app.get("/evaluate")
def evaluate_metrics():
    """Evaluates recommendation metrics on synthetic benchmark data."""
    students = _load_students()
    fields = _load_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'évaluation indisponibles.")

    eval_records = []
    for s in students:
        recs = rank_fields_for_student(s, fields, top_k=5)
        rec_ids = [r.field_id for r in recs]

        # Ground truth simulation based on student profile goals/category
        ground_truth = []
        cat_tag = s.context.dict().get("category_tag", "")
        if "scientific" in cat_tag or "technical" in cat_tag:
            ground_truth = ["FIELD_INFO_01", "FIELD_ELEC_01", "FIELD_STAT_01", "FIELD_MED_01"]
        elif "literary" in cat_tag:
            ground_truth = ["FIELD_LAW_01", "FIELD_ECON_01"]
        else:
            ground_truth = ["FIELD_INFO_01", "FIELD_ECON_01", "FIELD_AGRO_01"]

        eval_records.append({
            "actual_relevant": ground_truth,
            "recommended": rec_ids
        })

    return evaluate_system_performance(eval_records, k=5)
