import pytest
from app.models.schemas import StudentProfile, FieldProfile, AcademicProfile, InterestProfile, AptitudeProfile, PreferenceProfile, ConstraintProfile
from app.services.counterfactual import simulate_counterfactual_improvements
from app.services.comparator import compare_fields
from app.services.action_plan import generate_action_plan
from app.services.feedback import record_human_feedback, get_all_feedback

@pytest.fixture
def sample_student():
    return StudentProfile(
        student_id="STU_SERV_TEST",
        academic=AcademicProfile(
            level="Terminale",
            series="D",
            records=[{"subject": "mathematics", "score": 10.0, "coefficient": 4.0}]
        ),
        interests=InterestProfile(technology=0.8),
        aptitudes=AptitudeProfile(),
        preferences=PreferenceProfile(),
        constraints=ConstraintProfile()
    )

@pytest.fixture
def sample_field():
    return FieldProfile(
        field_id="FIELD_INFO",
        name="Informatique",
        category="Informatique",
        academic_requirements={"mathematics": 0.9},
        required_min_grades={"mathematics": 12.0},
        mandatory_bac_series=["C", "D"],
        interest_profile={"technology": 0.9},
        aptitude_profile={"logic": 0.8},
        source="Test Source",
        verified_at="2024-06-30"
    )

def test_counterfactual_simulation(sample_student, sample_field):
    sim = simulate_counterfactual_improvements(sample_student, sample_field, {"mathematics": 3.0})
    assert sim["simulated_compatibility_score"] >= sim["initial_compatibility_score"]
    assert "disclaimer" in sim

def test_field_comparator(sample_student, sample_field):
    res = compare_fields(sample_student, [sample_field])
    assert res["compared_fields_count"] == 1
    assert len(res["comparison"]) == 1

def test_action_plan_generation(sample_student, sample_field):
    plan = generate_action_plan(sample_student, sample_field)
    assert plan["target_field_id"] == "FIELD_INFO"
    assert "roadmap" in plan

def test_human_feedback_logging():
    fb = record_human_feedback(
        recommendation_id="REC_001",
        expert_id="EXP_001",
        decision="accepted",
        reason="Excellente adéquation."
    )
    assert fb.decision == "accepted"
    assert len(get_all_feedback()) > 0
