import numpy as np
from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile

def calculate_interest_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    """
    Computes interest compatibility (0.0 to 1.0) using normalized cosine similarity
    between the student's interest vector and the field's expected interest profile.
    """
    positives = []
    warnings = []

    student_interests = student.interests.model_dump()
    field_interests = field.interest_profile

    # Align vectors across all field keys
    keys = list(field_interests.keys())
    if not keys:
        return 0.5, positives, warnings

    v_student = np.array([student_interests.get(k, 0.0) for k in keys], dtype=float)
    v_field = np.array([field_interests.get(k, 0.0) for k in keys], dtype=float)

    norm_s = np.linalg.norm(v_student)
    norm_f = np.linalg.norm(v_field)

    if norm_s == 0 or norm_f == 0:
        return 0.3, positives, ["Les centres d'intérêt renseignés sont faibles ou incomplets."]

    cosine_sim = np.dot(v_student, v_field) / (norm_s * norm_f)

    # Identify key alignment factors
    for k in keys:
        s_val = student_interests.get(k, 0.0)
        f_val = field_interests.get(k, 0.0)
        if f_val >= 0.7 and s_val >= 0.7:
            positives.append(f"Fort intérêt partagé pour le domaine : {k}.")
        elif f_val >= 0.7 and s_val < 0.4:
            warnings.append(f"Faible intérêt exprimé pour le domaine clé : {k}.")

    final_score = float(max(0.0, min(1.0, cosine_sim)))
    return final_score, positives, warnings
