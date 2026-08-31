from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile
from app.recommendation.translations import translate_key

def calculate_academic_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    positives = []
    warnings = []

    academic = student.academic
    if not academic.records:
        return 0.5, positives, ["Aucun historique de notes renseigné."]

    student_grades = {rec.subject.lower(): rec.score for rec in academic.records}

    weighted_sum = 0.0
    total_weights = 0.0

    for req_subject, req_weight in field.academic_requirements.items():
        sub_key = req_subject.lower()
        sub_fr = translate_key(req_subject)

        if sub_key in student_grades:
            grade = student_grades[sub_key]
            weighted_sum += (grade / 20.0) * req_weight
            total_weights += req_weight

            min_grade = field.required_min_grades.get(req_subject, 10.0)
            if grade >= min_grade + 2.0:
                positives.append(f"Excellentes notes en {sub_fr} ({grade:.1f}/20 vs min requis {min_grade:.1f}/20).")
            elif grade < min_grade:
                warnings.append(f"Note insuffisante en {sub_fr} ({grade:.1f}/20 vs min requis {min_grade:.1f}/20).")
        else:
            weighted_sum += 0.5 * req_weight
            total_weights += req_weight
            warnings.append(f"Information manquante pour la matière clé: {sub_fr}.")

    base_score = weighted_sum / total_weights if total_weights > 0 else 0.5

    if academic.progression_trend > 0:
        base_score += min(0.05, academic.progression_trend * 0.02)
        positives.append("Progression positive constatée dans les résultats récents.")
    elif academic.progression_trend < 0:
        base_score += max(-0.05, academic.progression_trend * 0.02)
        warnings.append("Baisse constatée dans la progression des notes récentes.")

    final_score = max(0.0, min(1.0, base_score))
    return final_score, positives, warnings
