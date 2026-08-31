from typing import Dict, Any, List
from app.models.schemas import StudentProfile, FieldProfile, AcademicRecord
from app.recommendation.ranking import rank_fields_for_student

def simulate_counterfactual_improvements(
    student: StudentProfile,
    target_field: FieldProfile,
    subject_improvements: Dict[str, float]
) -> Dict[str, Any]:
    """
    Simulates: "What if I improve my grade in Subject X by Y points?"
    Returns current score vs simulated score and estimated score gain.
    """
    # 1. Baseline calculation
    baseline_res = rank_fields_for_student(student, [target_field], top_k=1)[0]
    initial_score = baseline_res.global_score
    initial_acad_score = baseline_res.breakdown.academic_score

    # 2. Clone student profile and apply simulated grade improvements
    simulated_student = student.model_copy(deep=True)

    existing_records = {rec.subject.lower(): rec for rec in simulated_student.academic.records}
    for sub, boost in subject_improvements.items():
        sub_key = sub.lower()
        if sub_key in existing_records:
            existing_records[sub_key].score = min(20.0, existing_records[sub_key].score + boost)
        else:
            simulated_student.academic.records.append(
                AcademicRecord(
                    subject=sub,
                    score=min(20.0, 10.0 + boost),
                    coefficient=1.0
                )
            )

    simulated_res = rank_fields_for_student(simulated_student, [target_field], top_k=1)[0]
    simulated_score = simulated_res.global_score
    simulated_acad_score = simulated_res.breakdown.academic_score

    gain_percent = round((simulated_score - initial_score) * 100, 2)

    recommendations_list = []
    for sub, boost in subject_improvements.items():
        recommendations_list.append(f"Améliorer {sub} de +{boost:.1f} pts (Gain estimé: +{gain_percent}% sur la compatibilité globale).")

    return {
        "field_id": target_field.field_id,
        "field_name": target_field.name,
        "initial_compatibility_score": initial_score,
        "simulated_compatibility_score": simulated_score,
        "estimated_gain_percentage": gain_percent,
        "initial_academic_score": initial_acad_score,
        "simulated_academic_score": simulated_acad_score,
        "recommendations": recommendations_list,
        "disclaimer": "Cette estimation est une simulation indicative basée sur la structure actuelle du profil."
    }
