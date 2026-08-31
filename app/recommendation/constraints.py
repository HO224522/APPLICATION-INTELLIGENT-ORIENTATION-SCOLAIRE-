from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile

def evaluate_constraints(student: StudentProfile, field: FieldProfile) -> Tuple[bool, float, List[str], List[str]]:
    hard_violations = []
    feasibility_warnings = []

    # 1. HARD CONSTRAINT CHECK: BAC Series Eligibility
    eligibility = True
    student_series = student.academic.series.upper().strip() if student.academic.series else None
    mandatory_series_normalized = [s.upper().strip() for s in field.mandatory_bac_series]

    if mandatory_series_normalized:
        if not student_series:
            eligibility = False
            hard_violations.append("Série de BAC non renseignée pour vérifier l'éligibilité administrative officielle.")
        elif student_series not in mandatory_series_normalized:
            eligibility = False
            hard_violations.append(
                f"Série BAC {student_series} non admise officiellement. "
                f"Séries requises par CampusFaso : {', '.join(field.mandatory_bac_series)}."
            )

    # 2. SOFT CONSTRAINT CHECK: Feasibility Score Calculation
    feasibility_score = 1.0
    constraints = student.constraints

    if constraints.max_budget_xof is not None and field.indicative_cost_xof > 0:
        if field.indicative_cost_xof > constraints.max_budget_xof:
            feasibility_score -= 0.4
            feasibility_warnings.append(
                f"Coût indicatif ({field.indicative_cost_xof:,.0f} XOF) supérieur au budget disponible "
                f"({constraints.max_budget_xof:,.0f} XOF). Bourse ou financement complémentaire requis."
            )
        else:
            feasibility_score += 0.05

    if constraints.preferred_region and field.available_regions:
        if constraints.preferred_region not in field.available_regions:
            if not student.preferences.geographical_mobility:
                feasibility_score -= 0.3
                feasibility_warnings.append(
                    f"Formation dispensée à {', '.join(field.available_regions)} "
                    f"alors que la mobilité géographique déclarée est restreinte."
                )
            else:
                feasibility_score -= 0.1
                feasibility_warnings.append(
                    f"Nécessite une mobilité géographique vers {', '.join(field.available_regions)}."
                )

    feasibility_score = float(max(0.0, min(1.0, feasibility_score)))
    return eligibility, feasibility_score, hard_violations, feasibility_warnings
