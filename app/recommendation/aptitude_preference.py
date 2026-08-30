from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile

def calculate_aptitude_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    """
    Computes aptitude compatibility (0.0 to 1.0).
    Explicitly distinguishes DECLARED aptitudes from OBSERVED/MEASURED aptitudes.
    Observed aptitudes carry 70% weight when available, declared carry 30%.
    """
    positives = []
    warnings = []

    aptitudes = student.aptitudes
    field_apts = field.aptitude_profile

    total_score = 0.0
    total_weights = 0.0

    for apt_name, field_weight in field_apts.items():
        declared_val = getattr(aptitudes, f"declared_{apt_name}", 0.0)
        observed_val = getattr(aptitudes, f"observed_{apt_name}", None)

        if observed_val is not None:
            effective_apt = 0.7 * observed_val + 0.3 * declared_val
            positives.append(f"Aptitude mesurée/observée pour {apt_name} prise en compte.")
        else:
            effective_apt = declared_val
            warnings.append(f"Aptitude {apt_name} uniquement basée sur une auto-déclaration.")

        total_score += effective_apt * field_weight
        total_weights += field_weight

    score = total_score / total_weights if total_weights > 0 else 0.5
    return float(max(0.0, min(1.0, score))), positives, warnings

def calculate_preference_score(student: StudentProfile, field: FieldProfile) -> Tuple[float, List[str], List[str]]:
    """
    Computes preference alignment (study duration, practical vs theoretical style, mobility).
    """
    positives = []
    warnings = []
    score = 1.0

    pref = student.preferences

    # Study duration check
    if pref.preferred_study_duration == "short" and field.duration_years > 3:
        score -= 0.3
        warnings.append(f"Durée d'étude ({field.duration_years} ans) supérieure à la préférence d'études courtes.")
    elif pref.preferred_study_duration == "long" and field.duration_years >= 5:
        positives.append("Filière longue correspondant aux ambitions de l'élève.")

    # Study style matching
    if pref.study_style != "balanced" and field.study_style != "balanced":
        if pref.study_style == field.study_style:
            score += 0.1
            positives.append(f"Style de formation ({field.study_style}) parfaitement aligné.")
        else:
            score -= 0.2
            warnings.append(f"Divergence entre style d'apprentissage ({pref.study_style}) et filière ({field.study_style}).")

    return float(max(0.0, min(1.0, score))), positives, warnings
