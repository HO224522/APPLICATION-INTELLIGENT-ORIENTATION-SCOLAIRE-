import pytest
from app.models.schemas import StudentProfile, FieldProfile, AcademicProfile, InterestProfile, AptitudeProfile, PreferenceProfile, ConstraintProfile
from app.recommendation.academic import calculate_academic_score
from app.recommendation.interest import calculate_interest_score
from app.recommendation.aptitude_preference import calculate_aptitude_score, calculate_preference_score
from app.recommendation.constraints import evaluate_constraints
from app.recommendation.ranking import rank_fields_for_student

@pytest.fixture
def sample_student():
    return StudentProfile(
        student_id="STU_TEST",
        academic=AcademicProfile(
            level="Terminale",
            series="C",
            records=[
                {"subject": "mathematics", "score": 16.0, "coefficient": 4.0},
                {"subject": "physics", "score": 14.0, "coefficient": 4.0},
                {"subject": "french", "score": 12.0, "coefficient": 3.0}
            ],
            progression_trend=0.5
        ),
        interests=InterestProfile(technology=0.9, problem_solving=0.85),
        aptitudes=AptitudeProfile(declared_logic=0.8, observed_logic=0.9),
        preferences=PreferenceProfile(preferred_study_duration="long", study_style="practical"),
        constraints=ConstraintProfile(max_budget_xof=400000.0, preferred_region="Ouagadougou")
    )

@pytest.fixture
def sample_field():
    return FieldProfile(
        field_id="FIELD_INFO",
        name="Informatique",
        category="Informatique",
        academic_requirements={"mathematics": 0.9, "physics": 0.6, "french": 0.5},
        required_min_grades={"mathematics": 12.0},
        mandatory_bac_series=["C", "D", "E"],
        interest_profile={"technology": 0.9, "problem_solving": 0.8},
        aptitude_profile={"logic": 0.8},
        indicative_cost_xof=350000.0,
        available_regions=["Ouagadougou"],
        source="Test Source",
        verified_at="2024-06-30"
    )

def test_academic_scoring(sample_student, sample_field):
    score, pos, warn = calculate_academic_score(sample_student, sample_field)
    assert 0.0 <= score <= 1.0
    assert score > 0.7
    assert len(pos) > 0

def test_interest_scoring(sample_student, sample_field):
    score, pos, warn = calculate_interest_score(sample_student, sample_field)
    assert 0.0 <= score <= 1.0
    assert score > 0.8

def test_aptitude_scoring(sample_student, sample_field):
    score, pos, warn = calculate_aptitude_score(sample_student, sample_field)
    assert 0.0 <= score <= 1.0
    # Observed logic (0.9) weighted 70% vs declared logic (0.8) weighted 30% -> 0.87
    assert score >= 0.8

def test_constraints_evaluation(sample_student, sample_field):
    eligibility, feas_score, hard_viol, soft_warn = evaluate_constraints(sample_student, sample_field)
    assert eligibility is True
    assert feas_score >= 0.9
    assert len(hard_viol) == 0

def test_hard_constraint_violation(sample_student, sample_field):
    sample_student.academic.series = "A"  # BAC A ineligible for Informatique (C, D, E required)
    eligibility, feas_score, hard_viol, soft_warn = evaluate_constraints(sample_student, sample_field)
    assert eligibility is False
    assert len(hard_viol) > 0

def test_ranking_engine(sample_student, sample_field):
    recs = rank_fields_for_student(sample_student, [sample_field], top_k=1)
    assert len(recs) == 1
    assert recs[0].rank == 1
    assert recs[0].eligibility is True
