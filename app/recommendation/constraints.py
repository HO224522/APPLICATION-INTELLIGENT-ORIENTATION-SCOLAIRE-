from typing import Tuple, List
from app.models.schemas import StudentProfile, FieldProfile

def evaluate_constraints(student: StudentProfile, field: FieldProfile) -> Tuple[bool, float, List[str], List[str]]:
    """
    Distinguishes HARD CONSTRAINTS (Official Eligibility) from SOFT CONSTRAINTS (Feasibility).

    Hard constraints (Eligibility):
    - Mandatory BAC series check (e.g., BAC C, D, E required for Engineering/Medicine).

    Soft constraints (Feasibility):
    - Financial cost vs student constraint budget.
    - Regional availability vs student geographical mobility.

    Returns: (eligibility, feasibility_score, hard_violations, feasibility_warnings)
    """
    hard_violations = []
    feasibility_warnings = []

    # 1. HARD CONSTRAINT CHECK: BAC Series Eligibility
    eligibility = True
    student_series = student.academic.series.upper().strip() if student.academic.series else None
    mandatory_series_normalized = [s.upper().strip() for s in field.mandatory_bac_series]

    if mandatory_series_normalized:
        if not student_series:
            eligibility = False
            hard_violations.append("Série de BAC non renseignée pour vérifier l'éligibilité officielle.")
        elif student_series not in mandatory_series_normalized:
            eligibility = False
            hard_violations.append(
                f"Série BAC {student_series} non admise officiellement. "
                f"Séries requises: {', '.join(field.mandatory_bac_series)}."
            )

    # 2. SOFT CONSTRAINT CHECK: Feasibility Score Calculation
    feasibility_score = 1.0
    constraints = student.constraints

    # Budget feasibility check
    if constraints.max_budget_xof is not None and field.indicative_cost_xof > 0:
        if field.indicative_cost_xof > constraints.max_budget_xof:
            budget_gap = field.indicative_cost_xof - constraints.max_budget_xof
            feasibility_score -= 0.4
            feasibility_warnings.append(
                f"Coût indicatif ({field.indicative_cost_xof:,.0f} XOF) supérieur au budget déclaré "
                f"({constraints.max_budget_xof:,.0f} XOF). Un besoin de bourse/financement est identifié."
            )
        else:
            feasibility_score += 0.05

    # Location / Mobility feasibility check
    if constraints.preferred_region and field.available_regions:
        if constraints.preferred_region not in field.available_regions:
            if not student.preferences.geographical_mobility:
                feasibility_score -= 0.3
                feasibility_warnings.append(
                    f"Formation dispensée uniquement à {', '.join(field.available_regions)} "
                    f"alors que la mobilité géographique est restreinte."
                )
            else:
                feasibility_score -= 0.1
                feasibility_warnings.append(
                    f"Nécessite un déplacement géographique vers {', '.join(field.available_regions)}."
                )

    feasibility_score = float(max(0.0, min(1.0, feasibility_score)))
    return eligibility, feasibility_score, hard_violations, feasibility_warnings
