from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile

def calculate_academic_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    """
    Calculates academic compatibility score (0.0 to 1.0) based on weighted subject scores
    and subject requirements of the target field profile.
    Returns: (academic_score, positive_factors, warning_factors)
    """
    positives = []
    warnings = []

    academic = student.academic
    if not academic.records:
        return 0.5, positives, ["Aucun historique de notes renseigné."]

    # Convert student records into a grade lookup (out of 20)
    student_grades = {rec.subject.lower(): rec.score for rec in academic.records}

    weighted_sum = 0.0
    total_weights = 0.0

    for req_subject, req_weight in field.academic_requirements.items():
        sub_key = req_subject.lower()
        if sub_key in student_grades:
            grade = student_grades[sub_key]
            weighted_sum += (grade / 20.0) * req_weight
            total_weights += req_weight

            # Check threshold warning
            min_grade = field.required_min_grades.get(req_subject, 10.0)
            if grade >= min_grade + 2.0:
                positives.append(f"Excellentes notes en {req_subject} ({grade:.1f}/20 vs min {min_grade:.1f}/20).")
            elif grade < min_grade:
                warnings.append(f"Note insuffisante en {req_subject} ({grade:.1f}/20 vs min requis {min_grade:.1f}/20).")
        else:
            # Subject missing from student records, assume neutral base average (10/20)
            weighted_sum += 0.5 * req_weight
            total_weights += req_weight
            warnings.append(f"Information manquante pour la matière clé: {req_subject}.")

    base_score = weighted_sum / total_weights if total_weights > 0 else 0.5

    # Adjustment for overall progression trend (+0.05 max for positive trend)
    if academic.progression_trend > 0:
        base_score += min(0.05, academic.progression_trend * 0.02)
        positives.append("Progression positive constatée dans les résultats scolaires.")
    elif academic.progression_trend < 0:
        base_score += max(-0.05, academic.progression_trend * 0.02)
        warnings.append("Baisse constatée dans la progression des notes récentes.")

    # Clamp score between 0.0 and 1.0
    final_score = max(0.0, min(1.0, base_score))
    return final_score, positives, warnings
