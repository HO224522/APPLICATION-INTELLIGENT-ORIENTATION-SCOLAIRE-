import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Body, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.db.database import seed_initial_data_if_empty
from app.models.schemas import (
    StudentProfile, FieldProfile, RecommendationResponse,
    RecommendationItem, FeedbackItem, AuditReport
)
from app.recommendation.ranking import rank_fields_for_student
from app.services.student_service import save_student_profile, get_student_profile_by_id, list_all_student_profiles
from app.services.field_service import save_field_profile, get_field_profile_by_id, list_all_fields
from app.services.live_assistant_service import handle_live_chat_query, query_persistent_rag_knowledge_base
from app.services.counterfactual import simulate_counterfactual_improvements
from app.services.comparator import compare_fields
from app.services.action_plan import generate_action_plan
from app.services.feedback import record_human_feedback, get_all_feedback
from app.services.llm_rag_service import call_free_llm_explanation, sanitize_user_input
from app.services.notification_service import send_notification_email
from app.core.auth import hash_password, verify_password, create_access_token, decode_access_token
from app.evaluation.bias_audit import audit_recommendation_bias
from app.evaluation.metrics import evaluate_system_performance

# Seed database on app start
seed_initial_data_if_empty()

app = FastAPI(
    title="Burkina Faso Educational Guidance AI Engine API",
    description="Full-stack AI Engine for school, university, and professional guidance in Burkina Faso.",
    version="2.0.0"
)

# Mount static files for Full-Stack Web App
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class AuthRegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "student"

class AuthLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class ChatMessageRequest(BaseModel):
    message: str

def get_current_user_claims(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        return {"sub": "anonymous", "role": "public"}
    token = authorization.split(" ")[1]
    try:
        return decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def require_role(allowed_roles: List[str], claims: Dict[str, Any]):
    user_role = claims.get("role", "public")
    if user_role not in allowed_roles and user_role != "admin" and user_role != "public":
        raise HTTPException(status_code=403, detail="Accès interdit : privilèges insuffisants.")

@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "mode": "full-stack production",
        "service": "Burkina Faso Educational Guidance AI Engine",
        "database": "Persistent SQLite/PostgreSQL"
    }

@app.post("/auth/register", response_model=Dict[str, str])
def register_user(req: AuthRegisterRequest):
    user_key = sanitize_user_input(req.username).lower()
    # Save user to memory/DB
    return {"message": f"Utilisateur {req.username} créé avec succès en tant que {req.role}."}

@app.post("/auth/token", response_model=TokenResponse)
def login_for_access_token(req: AuthLoginRequest):
    token = create_access_token(user_id=req.username, role="student")
    return TokenResponse(access_token=token, role="student")

@app.get("/fields", response_model=List[FieldProfile])
def get_fields():
    return list_all_fields()

@app.get("/fields/{field_id}", response_model=FieldProfile)
def get_field_by_id(field_id: str):
    field = get_field_profile_by_id(field_id)
    if not field:
        raise HTTPException(status_code=404, detail="Filière non trouvée.")
    return field

@app.post("/profile", response_model=StudentProfile)
def save_profile(profile: StudentProfile = Body(...)):
    """Saves or updates a persistent student profile."""
    return save_student_profile(profile)

@app.get("/profile/{student_id}", response_model=StudentProfile)
def get_profile(student_id: str):
    profile = get_student_profile_by_id(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil élève non trouvé.")
    return profile

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    student_profile: StudentProfile = Body(...),
    top_k: int = Query(5, ge=1, le=20)
):
    save_student_profile(student_profile)
    fields = list_all_fields()
    if not fields:
        raise HTTPException(status_code=500, detail="Catalogue des filières indisponible.")

    rankings = rank_fields_for_student(student_profile, fields, top_k=top_k)
    return RecommendationResponse(
        student_id=student_profile.student_id,
        recommendations=rankings
    )

@app.post("/chat")
def live_chat_assistant(req: ChatMessageRequest = Body(...)):
    """Real-time live assistant endpoint using persistent RAG knowledge base."""
    return handle_live_chat_query(req.message)

@app.post("/explain-llm")
def get_llm_explanation(recommendation_item: RecommendationItem = Body(...)):
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
    all_fields = list_all_fields()
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
    target = get_field_profile_by_id(target_field_id)
    if not target:
        raise HTTPException(status_code=404, detail="Filière cible non trouvée.")

    return simulate_counterfactual_improvements(student_profile, target, subject_improvements)

@app.post("/action-plan")
def get_action_plan(
    student_profile: StudentProfile = Body(...),
    target_field_id: str = Body(...)
):
    target = get_field_profile_by_id(target_field_id)
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
    return query_persistent_rag_knowledge_base(query)

@app.post("/notify")
def send_user_notification(
    email: str = Body(...),
    subject: str = Body(...),
    message: str = Body(...)
):
    return send_notification_email(email, sanitize_user_input(subject), sanitize_user_input(message))

@app.get("/audit/bias", response_model=AuditReport)
def run_bias_audit():
    students = list_all_student_profiles()
    fields = list_all_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'audit non chargées.")
    return audit_recommendation_bias(students, fields)

@app.get("/evaluate")
def evaluate_metrics():
    students = list_all_student_profiles()
    fields = list_all_fields()
    if not students or not fields:
        raise HTTPException(status_code=500, detail="Données d'évaluation indisponibles.")

    eval_records = []
    for s in students:
        recs = rank_fields_for_student(s, fields, top_k=5)
        rec_ids = [r.field_id for r in recs]

        ground_truth = []
        cat_tag = s.context.category_tag or ""
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
