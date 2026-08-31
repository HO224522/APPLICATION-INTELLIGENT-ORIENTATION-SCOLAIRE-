import json
import random

def generate_100_synthetic_students(output_path: str = "data/synthetic/students.json"):
    categories = [
        "excellent_scientific", "average_scientific", "literary_profile",
        "technical_profile", "undecided", "financial_constrained",
        "incomplete_data", "contradictory_profile"
    ]

    series_list = ["C", "D", "A", "E", "F2", "F3", "G2"]
    cities = ["Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Ouahigouya", "Fada N'Gourma"]
    genders = ["M", "F"]

    students = []

    for i in range(1, 101):
        cat = categories[(i - 1) % len(categories)]
        gender = genders[i % 2]
        city = cities[i % len(cities)]

        # Base template
        student_id = f"SYNTH_STU_{i:03d}"

        if cat == "excellent_scientific":
            series = "C" if i % 2 == 0 else "D"
            math_grade = random.uniform(15.0, 19.5)
            phys_grade = random.uniform(14.5, 19.0)
            fr_grade = random.uniform(12.0, 16.0)
            tech_int = random.uniform(0.8, 1.0)
            prob_int = random.uniform(0.8, 1.0)
            budget = random.choice([300000.0, 500000.0, 1000000.0])
            observed_logic = random.uniform(0.85, 0.98)
        elif cat == "average_scientific":
            series = "D"
            math_grade = random.uniform(10.0, 13.5)
            phys_grade = random.uniform(10.0, 13.0)
            fr_grade = random.uniform(10.0, 14.0)
            tech_int = random.uniform(0.5, 0.8)
            prob_int = random.uniform(0.6, 0.8)
            budget = 350000.0
            observed_logic = random.uniform(0.6, 0.75)
        elif cat == "literary_profile":
            series = "A"
            math_grade = random.uniform(6.0, 10.0)
            phys_grade = random.uniform(5.0, 9.0)
            fr_grade = random.uniform(14.0, 18.0)
            tech_int = random.uniform(0.1, 0.4)
            prob_int = random.uniform(0.4, 0.6)
            budget = 250000.0
            observed_logic = None
        elif cat == "technical_profile":
            series = "F2" if i % 2 == 0 else "F3"
            math_grade = random.uniform(11.0, 14.0)
            phys_grade = random.uniform(12.0, 16.0)
            fr_grade = random.uniform(9.0, 12.0)
            tech_int = random.uniform(0.85, 1.0)
            prob_int = random.uniform(0.7, 0.9)
            budget = 400000.0
            observed_logic = random.uniform(0.75, 0.9)
        elif cat == "financial_constrained":
            series = "D"
            math_grade = random.uniform(12.0, 16.0)
            phys_grade = random.uniform(11.0, 15.0)
            fr_grade = random.uniform(11.0, 14.0)
            tech_int = random.uniform(0.7, 0.9)
            prob_int = random.uniform(0.7, 0.9)
            budget = 50000.0  # Very tight budget constraint
            observed_logic = random.uniform(0.7, 0.85)
        elif cat == "incomplete_data":
            series = None
            math_grade = 11.0
            phys_grade = 10.0
            fr_grade = 11.0
            tech_int = 0.5
            prob_int = 0.5
            budget = None
            observed_logic = None
        elif cat == "contradictory_profile":
            series = "A"
            math_grade = 7.0
            phys_grade = 6.0
            fr_grade = 15.0
            tech_int = 0.95  # Declares tech interest despite low math and literary series
            prob_int = 0.90
            budget = 300000.0
            observed_logic = 0.40
        else:  # undecided
            series = "D"
            math_grade = random.uniform(10.0, 12.0)
            phys_grade = random.uniform(10.0, 12.0)
            fr_grade = random.uniform(10.0, 12.0)
            tech_int = 0.5
            prob_int = 0.5
            budget = 200000.0
            observed_logic = None

        profile = {
            "student_id": student_id,
            "academic": {
                "level": "Terminale",
                "series": series,
                "records": [
                    {"subject": "mathematics", "score": round(math_grade, 1), "coefficient": 4.0},
                    {"subject": "physics", "score": round(phys_grade, 1), "coefficient": 4.0},
                    {"subject": "french", "score": round(fr_grade, 1), "coefficient": 3.0},
                    {"subject": "philosophy", "score": round(random.uniform(8.0, 14.0), 1), "coefficient": 2.0}
                ],
                "overall_average": round((math_grade + phys_grade + fr_grade) / 3.0, 2),
                "progression_trend": round(random.uniform(-0.5, 0.8), 2)
            },
            "interests": {
                "technology": round(tech_int, 2),
                "problem_solving": round(prob_int, 2),
                "health": 0.9 if cat == "excellent_scientific" and i % 2 == 0 else 0.2,
                "law": 0.85 if cat == "literary_profile" else 0.2,
                "economy": 0.7 if cat == "undecided" else 0.3
            },
            "aptitudes": {
                "declared_logic": round(prob_int, 2),
                "observed_logic": round(observed_logic, 2) if observed_logic is not None else None,
                "declared_communication": round(fr_grade / 20.0, 2)
            },
            "preferences": {
                "preferred_study_duration": "long" if cat == "excellent_scientific" else "short",
                "study_style": "practical" if cat in ["technical_profile", "financial_constrained"] else "balanced",
                "geographical_mobility": i % 3 != 0
            },
            "constraints": {
                "max_budget_xof": budget,
                "preferred_region": city,
                "has_financial_aid_need": cat == "financial_constrained"
            },
            "goals": ["Ingénieur", "Médecin"] if cat == "excellent_scientific" else ["Juriste"] if cat == "literary_profile" else [],
            "context": {
                "country": "Burkina Faso",
                "city": city,
                "gender": gender,
                "category_tag": cat
            }
        }
        students.append(profile)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)

    print(f"Generated 100 synthetic student profiles at {output_path}")

if __name__ == "__main__":
    generate_100_synthetic_students()
