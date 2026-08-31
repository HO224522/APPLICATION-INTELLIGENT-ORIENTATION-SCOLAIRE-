from typing import Dict, Any, List
from app.models.schemas import StudentProfile, FieldProfile
from app.recommendation.ranking import rank_fields_for_student

def generate_action_plan(
    student: StudentProfile,
    target_field: FieldProfile
) -> Dict[str, Any]:
    """
    Generates a personalized action plan:
    OBJECTIF -> ÉCARTS IDENTIFIÉS -> COMPÉTENCES À DÉVELOPPER -> MATIÈRES À RENFORCER -> FORMATIONS -> ÉCHÉANCES -> PROCHAINES ACTIONS
    """
    rec_item = rank_fields_for_student(student, [target_field], top_k=1)[0]

    # Identify gaps
    weak_subjects = []
    student_grades = {rec.subject.lower(): rec.score for rec in student.academic.records}
    for sub, min_g in target_field.required_min_grades.items():
        curr_g = student_grades.get(sub.lower(), 10.0)
        if curr_g < min_g:
            weak_subjects.append(f"{sub} (Actuel: {curr_g:.1f}/20 vs Requis: {min_g:.1f}/20)")

    return {
        "student_id": student.student_id,
        "target_field_id": target_field.field_id,
        "target_field_name": target_field.name,
        "current_compatibility_score": rec_item.global_score,
        "roadmap": {
            "objective": f"Intégrer une formation en {target_field.name}",
            "identified_gaps": rec_item.explanation.warning_factors + weak_subjects,
            "skills_to_develop": target_field.required_skills,
            "subjects_to_reinforce": weak_subjects if weak_subjects else ["Maintenir le niveau actuel dans les matières clés."],
            "formations_to_explore": target_field.institutions,
            "deadlines": [
                "Dépôt de candidature CampusFaso / Établissements : Juin - Juillet",
                "Validation des vœux d'orientation : Août",
                "Inscriptions universitaires : Septembre - Octobre"
            ],
            "immediate_actions": rec_item.next_steps
        }
    }
