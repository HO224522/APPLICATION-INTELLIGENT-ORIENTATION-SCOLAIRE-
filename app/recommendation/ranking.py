from typing import List
from app.core.config import settings
from app.models.schemas import StudentProfile, FieldProfile, RecommendationItem, CompatibilityBreakdown
from app.recommendation.academic import calculate_academic_score
from app.recommendation.interest import calculate_interest_score
from app.recommendation.aptitude_preference import calculate_aptitude_score, calculate_preference_score
from app.recommendation.constraints import evaluate_constraints
from app.recommendation.explanations import generate_explanation, calculate_confidence_score

def rank_fields_for_student(
    student: StudentProfile,
    fields: List[FieldProfile],
    top_k: int = 5
) -> List[RecommendationItem]:
    """
    Ranks candidate fields for a student profile using explicit hybrid scoring rules.
    Returns a sorted list of RecommendationItem.
    """
    results = []

    for field in fields:
        # 1. Academic Compatibility
        acad_score, acad_pos, acad_warn = calculate_academic_score(student, field)

        # 2. Interest Compatibility
        int_score, int_pos, int_warn = calculate_interest_score(student, field)

        # 3. Aptitude Compatibility
        apt_score, apt_pos, apt_warn = calculate_aptitude_score(student, field)

        # 4. Preference Score
        pref_score, pref_pos, pref_warn = calculate_preference_score(student, field)

        # 5. Constraints & Feasibility Score
        eligibility, feas_score, hard_violations, feas_warn = evaluate_constraints(student, field)

        # Goal Score (matching declared goals with career paths or field category)
        goal_score = 0.5
        if student.goals:
            for goal in student.goals:
                if goal.lower() in field.category.lower() or any(goal.lower() in cp.lower() for cp in field.career_paths):
                    goal_score = 0.95
                    acad_pos.append(f"Correspondance exacte avec l'objectif professionnel : {goal}.")
                    break

        # Weighted Hybrid Global Score
        global_score = (
            acad_score * settings.WEIGHT_ACADEMIC +
            int_score * settings.WEIGHT_INTEREST +
            apt_score * settings.WEIGHT_APTITUDE +
            pref_score * settings.WEIGHT_PREFERENCE +
            goal_score * settings.WEIGHT_GOAL +
            feas_score * settings.WEIGHT_FEASIBILITY
        )

        # Penalize global score if hard constraints are violated, but retain for ranking/awareness
        if not eligibility:
            global_score *= 0.4

        breakdown = CompatibilityBreakdown(
            academic_score=round(acad_score, 2),
            interest_score=round(int_score, 2),
            aptitude_score=round(apt_score, 2),
            preference_score=round(pref_score, 2),
            feasibility_score=round(feas_score, 2),
            global_score=round(global_score, 2)
        )

        positives = list(set(acad_pos + int_pos + apt_pos + pref_pos))
        warnings = list(set(acad_warn + int_warn + apt_warn + pref_warn))

        explanation = generate_explanation(
            student=student,
            field=field,
            positive_factors=positives,
            warning_factors=warnings,
            hard_violations=hard_violations,
            feasibility_warnings=feas_warn
        )

        confidence = calculate_confidence_score(student, field, eligibility)

        # Generate next steps
        next_steps = []
        if not eligibility:
            next_steps.append("Vérifier les passerelles ou équivalences pour satisfaire les critères administratifs requis.")
        if acad_score < 0.6:
            next_steps.append("Renforcer les matières scientifiques/techniques fondamentales associées à cette filière.")
        next_steps.append(f"Consulter la fiche détaillée des établissements dispensant {field.name} ({', '.join(field.institutions)}).")

        item = RecommendationItem(
            rank=0,  # Assigned after sorting
            field_id=field.field_id,
            field_name=field.name,
            category=field.category,
            global_score=round(global_score, 4),
            eligibility=eligibility,
            confidence_score=round(confidence, 2),
            breakdown=breakdown,
            explanation=explanation,
            next_steps=next_steps
        )
        results.append(item)

    # Sort primarily by eligibility (eligible first) then by global_score descending
    results.sort(key=lambda x: (x.eligibility, x.global_score), reverse=True)

    # Assign ranks and select top_k
    ranked_top_k = []
    for idx, item in enumerate(results[:top_k], start=1):
        item.rank = idx
        ranked_top_k.append(item)

    return ranked_top_k
