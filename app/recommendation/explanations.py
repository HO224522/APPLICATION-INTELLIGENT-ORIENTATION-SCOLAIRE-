from app.models.schemas import StudentProfile, FieldProfile, ExplanationDetails

def generate_explanation(
    student: StudentProfile,
    field: FieldProfile,
    positive_factors: list[str],
    warning_factors: list[str],
    hard_violations: list[str],
    feasibility_warnings: list[str]
) -> ExplanationDetails:
    """
    Constructs a clear, structured explanation object (JSON-formatted)
    that can be safely rendered or converted into natural language by an optional LLM layer.
    """
    missing_info = []

    # Missing info check
    if not student.academic.records:
        missing_info.append("Dossier scolaire incomplet (aucune note enregistrée).")
    if student.aptitudes.observed_logic is None and student.aptitudes.observed_communication is None:
        missing_info.append("Absence d'aptitudes mesurées/observées (uniquement des aptitudes auto-déclarées).")

    all_warnings = warning_factors + feasibility_warnings

    return ExplanationDetails(
        positive_factors=positive_factors,
        warning_factors=all_warnings,
        hard_constraints_violated=hard_violations,
        missing_information=missing_info
    )

def calculate_confidence_score(student: StudentProfile, field: FieldProfile, eligibility: bool) -> float:
    """
    Calculates recommendation confidence based on completeness of data and metadata trustworthiness.
    confidence != probability of success in life.
    """
    confidence = 0.5  # Base confidence

    # Academic completeness
    if student.academic.records:
        confidence += 0.2
    if student.academic.series:
        confidence += 0.1

    # Aptitude completeness (observed vs declared)
    if student.aptitudes.observed_logic is not None or student.aptitudes.observed_communication is not None:
        confidence += 0.1

    # Field verification metadata confidence
    confidence *= field.confidence_level

    if not eligibility:
        confidence *= 0.8  # Ineligible fields carry lower overall confidence

    return float(max(0.1, min(1.0, confidence)))
