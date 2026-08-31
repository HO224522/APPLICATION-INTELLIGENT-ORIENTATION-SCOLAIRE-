FRENCH_KEY_MAP = {
    # Subjects
    "mathematics": "Mathématiques",
    "physics": "Physique-Chimie",
    "french": "Français",
    "philosophy": "Philosophie",
    "english": "Anglais",
    "svt": "SVT (Sciences de la Vie et de la Terre)",
    "history_geo": "Histoire-Géographie",
    # Interests
    "technology": "Technologie",
    "health": "Santé",
    "science": "Sciences",
    "economy": "Économie",
    "law": "Droit",
    "letters": "Lettres & Langues",
    "arts": "Arts & Culture",
    "agriculture": "Agronomie & Agriculture",
    "engineering": "Sciences de l'Ingénieur",
    "computer_science": "Informatique",
    "commerce": "Commerce & Gestion",
    "problem_solving": "Résolution de problèmes",
    "people_oriented": "Relation humaine & Écoute",
    "machines_oriented": "Travail sur machines & Équipements",
    "data_oriented": "Analyse de données & Chiffres",
    "ideas_oriented": "Réflexion théorique & Idées",
    # Aptitudes
    "logic": "Raisonnement logique",
    "communication": "Communication orale et écrite",
    "creativity": "Créativité & Innovation",
    "organization": "Organisation & Méthode",
    "practical_work": "Travail pratique & Manipulation",
    "theoretical_work": "Travail théorique & Abstrait",
    # Study styles
    "practical": "Pratique & Appliqué",
    "theory": "Théorique & Académique",
    "balanced": "Équilibré (Théorie & Pratique)"
}

def translate_key(key: str) -> str:
    return FRENCH_KEY_MAP.get(key.lower(), key)
