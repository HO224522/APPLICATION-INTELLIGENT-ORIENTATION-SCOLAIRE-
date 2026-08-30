from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class AcademicRecord(BaseModel):
    subject: str  # e.g., "mathematics", "physics", "french", "philosophy"
    score: float  # Grade out of 20
    coefficient: float = 1.0

class AcademicProfile(BaseModel):
    level: str  # e.g., "Seconde", "Première", "Terminale", "BAC"
    class_name: Optional[str] = None
    series: Optional[str] = None  # e.g., "A", "C", "D", "E", "F1", "F2", "F3", "G2"
    records: List[AcademicRecord] = []
    overall_average: Optional[float] = None
    progression_trend: float = 0.0  # Positive for improvement, negative for decline
    strong_subjects: List[str] = []
    weak_subjects: List[str] = []

class InterestProfile(BaseModel):
    # Interest domain vector normalized (0.0 to 1.0)
    technology: float = 0.0
    health: float = 0.0
    science: float = 0.0
    economy: float = 0.0
    law: float = 0.0
    letters: float = 0.0
    arts: float = 0.0
    agriculture: float = 0.0
    engineering: float = 0.0
    computer_science: float = 0.0
    commerce: float = 0.0

    # Intrinsic drives
    problem_solving: float = 0.0
    people_oriented: float = 0.0
    machines_oriented: float = 0.0
    data_oriented: float = 0.0
    ideas_oriented: float = 0.0

class AptitudeProfile(BaseModel):
    # Declared vs Observed/Measured aptitudes (0.0 to 1.0)
    declared_logic: float = 0.0
    observed_logic: Optional[float] = None

    declared_communication: float = 0.0
    observed_communication: Optional[float] = None

    declared_creativity: float = 0.0
    observed_creativity: Optional[float] = None

    declared_organization: float = 0.0
    observed_organization: Optional[float] = None

    declared_practical_work: float = 0.0
    observed_practical_work: Optional[float] = None

    declared_theoretical_work: float = 0.0
    observed_theoretical_work: Optional[float] = None

class PreferenceProfile(BaseModel):
    preferred_study_duration: str = "long"  # "short" (BTS/DUT, 2-3 yrs), "long" (Master/Engineering, 5+ yrs)
    study_style: str = "balanced"  # "theory", "practical", "balanced"
    geographical_mobility: bool = True
    work_environment: Optional[str] = "indifferent"  # "team", "individual", "indifferent"

class ConstraintProfile(BaseModel):
    max_budget_xof: Optional[float] = None  # Financial budget in CFA Francs
    preferred_region: Optional[str] = "Ouagadougou"  # e.g., "Ouagadougou", "Bobo-Dioulasso", "Koudougou"
    mobility_limit: Optional[str] = None
    has_financial_aid_need: bool = False

class StudentContext(BaseModel):
    country: str = "Burkina Faso"
    city: Optional[str] = None
    gender: Optional[str] = None
    socioeconomic_status: Optional[str] = None

class StudentProfile(BaseModel):
    student_id: str
    academic: AcademicProfile
    interests: InterestProfile
    aptitudes: AptitudeProfile
    preferences: PreferenceProfile
    constraints: ConstraintProfile
    goals: List[str] = []
    context: StudentContext = Field(default_factory=StudentContext)

# Field Profile Schemas
class FieldProfile(BaseModel):
    field_id: str
    name: str
    category: str  # e.g., "Informatique", "Santé", "Agronomie", "Droit"
    academic_requirements: Dict[str, float]  # Subject weight requirements (0.0 to 1.0)
    required_min_grades: Dict[str, float] = {}  # Minimum grade out of 20 per required subject
    mandatory_bac_series: List[str] = []  # Official hard requirements, e.g. ["C", "D", "E"]
    interest_profile: Dict[str, float]  # Expected interest scores
    aptitude_profile: Dict[str, float]  # Expected aptitude scores
    study_style: str = "balanced"
    duration_years: int = 3
    indicative_cost_xof: float = 0.0
    available_regions: List[str] = ["Ouagadougou", "Bobo-Dioulasso"]
    institutions: List[str] = []
    career_paths: List[str] = []
    required_skills: List[str] = []

    # Metadata for verification & trustworthiness
    source: str
    verified_at: str
    confidence_level: float = 1.0

# Recommendation & Output Schemas
class CompatibilityBreakdown(BaseModel):
    academic_score: float
    interest_score: float
    aptitude_score: float
    preference_score: float
    feasibility_score: float
    global_score: float

class ExplanationDetails(BaseModel):
    positive_factors: List[str] = []
    warning_factors: List[str] = []
    hard_constraints_violated: List[str] = []
    missing_information: List[str] = []

class RecommendationItem(BaseModel):
    rank: int
    field_id: str
    field_name: str
    category: str
    global_score: float
    eligibility: bool  # Hard constraints status
    confidence_score: float
    breakdown: CompatibilityBreakdown
    explanation: ExplanationDetails
    next_steps: List[str] = []

class RecommendationResponse(BaseModel):
    student_id: str
    recommendations: List[RecommendationItem]

class FeedbackItem(BaseModel):
    recommendation_id: str
    expert_id: str
    decision: str  # "accepted", "modified", "rejected"
    suggested_field_id: Optional[str] = None
    reason: str
    timestamp: str

class AuditReport(BaseModel):
    total_profiles_audited: int
    parity_by_gender: Dict[str, Any]
    parity_by_region: Dict[str, Any]
    bias_detected: bool
    summary: str
