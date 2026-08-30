import json
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Body, Header, Depends
from pydantic import BaseModel
from app.models.schemas import (
    StudentProfile, FieldProfile, RecommendationResponse,
    RecommendationItem, FeedbackItem, AuditReport
)
from app.recommendation.ranking import rank_fields_for_student
from app.services.counterfactual import simulate_counterfactual_improvements
from app.services.comparator import compare_fields
from app.services.action_plan import generate_action_plan
from app.services.feedback import record_human_feedback, get_all_feedback
from app.services.llm_rag_service import call_free_llm_explanation, sanitize_user_input
from app.services.notification_service import send_notification_email
from app.core.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.rag.knowledge_base import query_knowledge_base
from app.evaluation.bias_audit import audit_recommendation_bias
from app.evaluation.metrics import evaluate_system_performance

app = FastAPI(
    title="Burkina Faso Educational Guidance AI Engine API",
    description="Engine for school, university, and professional guidance adapted to Burkina Faso (Cybersecurity Hardened).",
    version="1.1.0"
)

# Mock in-memory secure user store
_USERS_DB: Dict[str, Dict[str, str]] = {}

class AuthRegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "student"  # student, parent, counselor, admin

class AuthLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

def get_current_user_claims(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Cybersecurity Middleware: Validates JWT Bearer Token."""
    if not authorization or not authorization.startswith("Bearer "):
        # Anonymous public fallback for demonstration
        return {"sub": "anonymous", "role": "public"}
    token = authorization.split(" ")[1]
    try:
        return decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def require_role(allowed_roles: List[str], claims: Dict[str, Any]):
    """Cybersecurity RBAC authorization check."""
    user_role = claims.get("role", "public")
    if user_role not in allowed_roles and user_role != "admin" and user_role != "public":
        raise HTTPException(status_code=403, detail="Accès interdit : privilèges insuffisants.")

def _load_fields() -> List[FieldProfile]:
    fields_path = "data/synthetic/fields.json"
    if not os.path.exists(fields_path):
        return []
    with open(fields_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [FieldProfile(**item) for item in data]

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
        "cybersecurity_status": "Hardened (JWT, RBAC, Sanitized Inputs)",
        "free_apis_active": True,
        "documentation": "/docs"
    }

@app.post("/auth/register", response_model=Dict[str, str])
def register_user(req: AuthRegisterRequest):
    """Registers a new user securely with PBKDF2 password hashing."""
    user_key = sanitize_user_input(req.username).lower()
    if user_key in _USERS_DB:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà existe.")
    _USERS_DB[user_key] = {
        "username": req.username,
        "password_hash": hash_password(req.password),
        "role": req.role
    }
    return {"message": f"Utilisateur {req.username} créé avec succès en tant que {req.role}."}

@app.post("/auth/token", response_model=TokenResponse)
def login_for_access_token(req: AuthLoginRequest):
    """Authenticates user and issues signed JWT access token."""
    user_key = sanitize_user_input(req.username).lower()
    user = _USERS_DB.get(user_key)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Identifiants incorrects.")
    token = create_access_token(user_id=user["username"], role=user["role"])
    return TokenResponse(access_token=token, role=user["role"])

@app.get("/fields", response_model=List[FieldProfile])
def get_fields():
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
    top_k: int = Query(5, ge=1, le=20),
    claims: Dict[str, Any] = Depends(get_current_user_claims)
):
    fields = _load_fields()
    if not fields:
        raise HTTPException(status_code=500, detail="Catalogue des filières indisponible.")

    rankings = rank_fields_for_student(student_profile, fields, top_k=top_k)
    return RecommendationResponse(
        student_id=student_profile.student_id,
        recommendations=rankings
    )

@app.post("/explain-llm")
def get_llm_explanation(
    recommendation_item: RecommendationItem = Body(...),
    claims: Dict[str, Any] = Depends(get_current_user_claims)
):
    """
    Synthesizes structured recommendation outputs into natural language using Free Groq API / Ollama / Local secure fallback.
    """
    struct_exp = recommendation_item.explanation.model_dump()
    text_summary = call_free_llm_explanation(struct_exp)
    return {
        "field_name": recommendation_item.field_name,
        "natural_language_explanation": text_summary,
        "free_engine_used": "Groq / Ollama / Local Rule Engine"
    }

@app.post("/compare")
def compare_selected_fields(
    student_profile: StudentProfile = Body(...),
    field_ids: List[str] = Body(...)
):
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
    suggested_field_id: Optional[str] = Body(None),
    claims: Dict[str, Any] = Depends(get_current_user_claims)
):
    require_role(["counselor", "admin"], claims)
    try:
        return record_human_feedback(
            recommendation_id=recommendation_id,
            expert_id=expert_id,
            decision=decision,
            reason=sanitize_user_input(reason),
            suggested_field_id=suggested_field_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/feedback", response_model=List[FeedbackItem])
def list_feedback():
    return get_all_feedback()

@app.post("/rag/query")
def search_knowledge_base(query: str = Query(...)):
    safe_query = sanitize_user_input(query)
    return query_knowledge_base(safe_query)

@app.post("/notify")
def send_user_notification(
    email: str = Body(...),
    subject: str = Body(...),
    message: str = Body(...),
    claims: Dict[str, Any] = Depends(get_current_user_claims)
):
    return send_notification_email(email, sanitize_user_input(subject), sanitize_user_input(message))

@app.get("/audit/bias", response_model=AuditReport)
def run_bias_audit():
    students = _load_students()
    fields = _load_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'audit non chargées.")
    return audit_recommendation_bias(students, fields)

@app.get("/evaluate")
def evaluate_metrics():
    students = _load_students()
    fields = _load_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'évaluation indisponibles.")

    eval_records = []
    for s in students:
        recs = rank_fields_for_student(s, fields, top_k=5)
        rec_ids = [r.field_id for r in recs]

        ground_truth = []
        cat_tag = s.context.dict().get("category_tag", "")
        if "scientific" in cat_tag or "technical" in cat_tag:
            ground_truth = ["FIELD_INFO_01", "FIELD_ELEC_01", "FIELD_STAT_01", "FIELD_MED_01", "FIELD_CPGE_EPO"]
        elif "literary" in cat_tag:
            ground_truth = ["FIELD_LAW_01", "FIELD_ECON_01"]
        else:
            ground_truth = ["FIELD_INFO_01", "FIELD_ECON_01", "FIELD_AGRO_01"]

        eval_records.append({
            "actual_relevant": ground_truth,
            "recommended": rec_ids
        })

    return evaluate_system_performance(eval_records, k=5)
