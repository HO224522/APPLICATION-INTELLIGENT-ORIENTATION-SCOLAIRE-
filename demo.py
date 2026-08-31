#!/usr/bin/env python3
"""
MOTEUR D'ORIENTATION SCOLAIRE ET PROFESSIONNELLE DU BURKINA FASO
Interface de démonstration CLI (demo.py)
"""

import json
from app.models.schemas import StudentProfile, FieldProfile
from app.recommendation.ranking import rank_fields_for_student
from app.services.counterfactual import simulate_counterfactual_improvements
from app.services.action_plan import generate_action_plan
from app.evaluation.bias_audit import audit_recommendation_bias

def run_demo():
    print("==========================================================================")
    print("   MOTEUR D'INTELLIGENCE ARTIFICIELLE D'ORIENTATION - BURKINA FASO (MVP)")
    print("==========================================================================")
    print()

    # Load synthetic dataset
    with open("data/synthetic/fields.json", "r", encoding="utf-8") as f:
        fields = [FieldProfile(**item) for item in json.load(f)]

    with open("data/synthetic/students.json", "r", encoding="utf-8") as f:
        students = [StudentProfile(**item) for item in json.load(f)]

    sample_student = students[0]  # Excellent Scientific Profile

    print("PROFIL ÉLÈVE D'EXEMPLE")
    print("--------------------")
    print(f"Identifiant : {sample_student.student_id}")
    print(f"Niveau & Série : {sample_student.academic.level} - BAC Série {sample_student.academic.series}")
    print(f"Région : {sample_student.constraints.preferred_region} | Genre : {sample_student.context.gender}")
    print("Notes :")
    for rec in sample_student.academic.records:
        print(f"  - {rec.subject.capitalize()} : {rec.score:.1f}/20 (Coeff: {rec.coefficient})")
    print(f"Moyenne générale : {sample_student.academic.overall_average:.2f}/20")
    print(f"Intérêt technologie : {sample_student.interests.technology * 100:.0f}% | Résolution de problèmes : {sample_student.interests.problem_solving * 100:.0f}%")
    print(f"Aptitude logique observée : {sample_student.aptitudes.observed_logic * 100 if sample_student.aptitudes.observed_logic else 0:.0f}%")
    print()

    print("RECOMMANDATIONS TOP 5 (ANALYSE HYBRIDE ET CONTRAINTES)")
    print("------------------------------------------------------")
    recommendations = rank_fields_for_student(sample_student, fields, top_k=5)

    for item in recommendations:
        print(f"\n{item.rank}. {item.field_name.upper()} (Catégorie : {item.category})")
        print(f"   Compatibilité globale : {item.global_score * 100:.1f} % | Éligibilité officielle : {'ADMISA' if item.eligibility else 'NON ADMIS (Série non éligible)'}")
        print(f"   Confiance algorithmique : {item.confidence_score * 100:.0f} %")
        print(f"   Détail des scores : Académique={item.breakdown.academic_score*100:.0f}%, Intérêts={item.breakdown.interest_score*100:.0f}%, Aptitudes={item.breakdown.aptitude_score*100:.0f}%, Faisabilité={item.breakdown.feasibility_score*100:.0f}%")

        if item.explanation.positive_factors:
            print("   Facteurs favorables :")
            for pos in item.explanation.positive_factors:
                print(f"     + {pos}")

        if item.explanation.warning_factors:
            print("   Points de vigilance :")
            for warn in item.explanation.warning_factors:
                print(f"     - {warn}")

        if item.explanation.hard_constraints_violated:
            print("   Contraintes officielles non satisfaites :")
            for viol in item.explanation.hard_constraints_violated:
                print(f"     ! {viol}")

    print("\n==========================================================================")
    print("SIMULATION CONTRE-FACTUELLE ('Que dois-je améliorer ?')")
    print("------------------------------------------------------")
    target_field = fields[0]  # Informatique
    sim_res = simulate_counterfactual_improvements(sample_student, target_field, {"mathematics": 2.0})
    print(f"Filière visée : {sim_res['field_name']}")
    print(f"Compatibilité actuelle : {sim_res['initial_compatibility_score']*100:.1f}%")
    print(f"Compatibilité après +2.0 pts en Mathématiques : {sim_res['simulated_compatibility_score']*100:.1f}%")
    print(f"Gain estimé : +{sim_res['estimated_gain_percentage']}%")
    print(f"Note : {sim_res['disclaimer']}")

    print("\n==========================================================================")
    print("AUDIT DE BIAIS ET ÉQUITÉ DÉMOGRAPHIQUE (100 PROFILS SYNTHÉTIQUES)")
    print("------------------------------------------------------")
    audit = audit_recommendation_bias(students, fields)
    print(f"Profils audités : {audit.total_profiles_audited}")
    print(f"Biais discriminatoire détecté : {'OUI' if audit.bias_detected else 'NON'}")
    print(f"Synthèse : {audit.summary}")
    print("==========================================================================")

if __name__ == "__main__":
    run_demo()
