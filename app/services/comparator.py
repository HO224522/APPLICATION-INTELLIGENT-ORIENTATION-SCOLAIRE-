from typing import List, Dict, Any
from app.models.schemas import StudentProfile, FieldProfile
from app.recommendation.ranking import rank_fields_for_student

def compare_fields(
    student: StudentProfile,
    fields: List[FieldProfile]
) -> Dict[str, Any]:
    """
    Side-by-side comparison of 2+ fields for a specific student profile.
    """
    rankings = rank_fields_for_student(student, fields, top_k=len(fields))
    comparison_table = []

    for item in rankings:
        field_obj = next((f for f in fields if f.field_id == item.field_id), None)
        comparison_table.append({
            "field_id": item.field_id,
            "field_name": item.field_name,
            "category": item.category,
            "compatibility_score": item.global_score,
            "eligibility": item.eligibility,
            "duration_years": field_obj.duration_years if field_obj else None,
            "indicative_cost_xof": field_obj.indicative_cost_xof if field_obj else 0.0,
            "academic_score": item.breakdown.academic_score,
            "interest_score": item.breakdown.interest_score,
            "aptitude_score": item.breakdown.aptitude_score,
            "feasibility_score": item.breakdown.feasibility_score,
            "positive_factors": item.explanation.positive_factors,
            "warning_factors": item.explanation.warning_factors,
            "hard_violations": item.explanation.hard_constraints_violated,
            "institutions": field_obj.institutions if field_obj else [],
            "career_paths": field_obj.career_paths if field_obj else []
        })

    return {
        "student_id": student.student_id,
        "compared_fields_count": len(fields),
        "comparison": comparison_table
    }
