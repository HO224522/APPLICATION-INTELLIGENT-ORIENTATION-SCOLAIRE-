import numpy as np
from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile
from app.recommendation.translations import translate_key

def calculate_interest_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    positives = []
    warnings = []

    student_interests = student.interests.model_dump()
    field_interests = field.interest_profile

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

    for k in keys:
        s_val = student_interests.get(k, 0.0)
        f_val = field_interests.get(k, 0.0)
        k_fr = translate_key(k)
        if f_val >= 0.7 and s_val >= 0.7:
            positives.append(f"Fort intérêt partagé pour le domaine : {k_fr}.")
        elif f_val >= 0.7 and s_val < 0.4:
            warnings.append(f"Faible intérêt exprimé pour le domaine clé : {k_fr}.")

    final_score = float(max(0.0, min(1.0, cosine_sim)))
    return final_score, positives, warnings
