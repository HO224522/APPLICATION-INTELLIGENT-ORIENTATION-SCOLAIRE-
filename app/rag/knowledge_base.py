from typing import List, Dict, Any

# Mock institutional verified document repository for Burkina Faso orientation
INSTITUTIONAL_DOCUMENTS = [
    {
        "doc_id": "BF_GOV_2024_01",
        "title": "Conditions Générales d'Admission au Baccalauréat et Orientations Universitaires au Burkina Faso",
        "institution": "Ministère de l'Enseignement Supérieur, de la Recherche et de I'Innovation (MESRI)",
        "source": "Journal Officiel du Burkina Faso",
        "verified_at": "2024-06-15",
        "content": "Les filières d'ingénierie et de médecine requièrent obligatoirement un Baccalauréat scientifique (Séries C, D, E). L'orientation sur la plateforme CampusFaso s'appuie sur la moyenne au Baccalauréat et les notes obtenues dans les matières fondamentales."
    },
    {
        "doc_id": "BF_GOV_2024_02",
        "title": "Guide des Bourses Nationales et Aides d'Étude CIOSPB",
        "institution": "Centre National des Œuvres Universitaires (CENOU) / CIOSPB",
        "source": "Guide de l'Étudiant CIOSPB 2024",
        "verified_at": "2024-07-01",
        "content": "Les bourses nationales de premier cycle sont attribuées selon des critères d'âge (moins de 22 ans pour la licence), de mérite académique (moyenne supérieure ou égale à 12/20 au Bac) et de situation sociale."
    },
    {
        "doc_id": "BF_UNIV_2024_03",
        "title": "Offre de Formation et Débouchés - Université Joseph Ki-Zerbo (UJKZ)",
        "institution": "Université Joseph Ki-Zerbo",
        "source": "Catalogue Officiel UJKZ",
        "verified_at": "2024-05-10",
        "content": "UJKZ propose des formations de Licence, Master et Doctorat en Informatique, Mathématiques, Physique, Chimie, Médecine, Droit et Économie. L'UFR/SEA accueille les étudiants titulaires de Bac C et D."
    }
]

def query_knowledge_base(query_text: str) -> Dict[str, Any]:
    """
    RAG Retriever for official documentary information ONLY.
    IMPORTANT: The RAG engine does NOT calculate student compatibility scores.
    It retrieves official documents on institutions, admission rules, scholarships, and deadlines.
    """
    query_lower = query_text.lower()
    matched_docs = []

    for doc in INSTITUTIONAL_DOCUMENTS:
        if any(term in doc["title"].lower() or term in doc["content"].lower() for term in query_lower.split()):
            matched_docs.append(doc)

    if not matched_docs:
        matched_docs = INSTITUTIONAL_DOCUMENTS  # Fallback to general documents

    return {
        "query": query_text,
        "matched_documents_count": len(matched_docs),
        "documents": matched_docs,
        "disclaimer": "Informations documentaires officielles extraites sous réserve de mise à jour par les institutions concernées."
    }
