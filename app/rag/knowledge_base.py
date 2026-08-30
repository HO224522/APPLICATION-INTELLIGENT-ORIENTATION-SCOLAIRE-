from typing import List, Dict, Any

# Official institutional document repository for Burkina Faso orientation (DGCOB, CampusFaso, Universities, CIOSPB)
INSTITUTIONAL_DOCUMENTS = [
    {
        "doc_id": "BF_MESRI_2025_CARTAGRAPHIE",
        "title": "Nouvelle Carte Universitaire et Référentiel des Formations Prioritaires du Burkina Faso",
        "institution": "Ministère de l'Enseignement Supérieur, de la Recherche et de l'Innovation (MESRI)",
        "source": "Arrêté Ministériel n°2025-245/MESRI/SG/DGESup & Carte Universitaire Officielle",
        "verified_at": "2025-08-20",
        "content": "La carte universitaire catégorise 17 Institutions d'Enseignement Supérieur et de Recherche (IESR) en 4 Universités Généralistes (UJKZ, UNB, UNZ, UV-BF) habilitées dans 9 domaines (Santé, Vétérinaire, Sciences & Techno, Droit, Économie, LSH, LLA, Agronomie, Éducation) et 13 IESR Spécialisées (UTS, LBO, UDOC, UYAT, EPO, ENS, et Centres Universitaires de Banfora, Dori, Gaoua, Kaya, Manga, Tenkodogo, Ziniaré). L'Université Polytechnique du Burkina (UPB/EPO) regroupe les CPGE et les formations d'Ingénierie stratégiques."
    },
    {
        "doc_id": "BF_DGCOB_2026_01",
        "title": "Semaine Nationale de l'Information et de l'Orientation Post-Baccalauréat (SIO) et Procédures DGCOB",
        "institution": "Direction Générale du Conseil à l'Orientation Universitaire et des Bourses (DGCOB / ex-CIOSPB)",
        "source": "Portail Officiel DGCOB (ciospb.gov.bf / dgcob.gov.bf)",
        "verified_at": "2026-01-15",
        "content": "La DGCOB (ex-CIOSPB) assure le conseil à l'orientation post-baccalauréat et la gestion de la Commission Nationale des Bourses d'Études et des Stages (CNBES). Les critères d'attribution des bourses nationales de premier cycle comprennent : l'âge (moins de 22 ans pour la Licence 1), le mérite académique (moyenne au BAC >= 12/20) et la situation socio-économique."
    },
    {
        "doc_id": "BF_CAMPUSFASO_2026_01",
        "title": "Plateforme Nationale d'Orientation et d'Inscription CampusFaso",
        "institution": "MESRI / CampusFaso (campusfaso.bf)",
        "source": "Guide de l'Usager CampusFaso 2025-2026",
        "verified_at": "2026-02-01",
        "content": "Toutes les demandes d'orientation post-BAC et d'inscriptions dans les universités publiques et instituts partenaires du Burkina Faso s'effectuent obligatoirement en ligne via www.campusfaso.bf. L'affectation dans les filières contingentées se fait par classement automatique selon la moyenne au BAC, les notes des matières spécifiques et les coefficients officiels."
    },
    {
        "doc_id": "BF_EPO_2025_CPGE",
        "title": "Concours de Recrutement aux Classes Préparatoires aux Grandes Écoles (CPGE - EPO / UPB)",
        "institution": "École Polytechnique de Ouagadougou (EPO / UPB)",
        "source": "Communiqué Officiel de Recrutement CPGE EPO",
        "verified_at": "2025-07-15",
        "content": "L'École Polytechnique de Ouagadougou recrute les bacheliers des séries scientifiques (BAC C, D, E) sur concours pour les filières MPSI (Maths, Physique, Sciences de l'Ingénieur) et PCSI. L'EPO abrite également l'IGIT (Génie Informatique, Génie Télécoms) et l'IGSIT (Génie Industriel, Génie Mécanique)."
    },
    {
        "doc_id": "BF_UJKZ_IBAM_2025",
        "title": "Offres de Formation Professionnelle de l'Institut Burkinabè des Arts et Métiers (IBAM - UJKZ)",
        "institution": "Université Joseph Ki-Zerbo (UJKZ)",
        "source": "Guide de l'Étudiant IBAM / UJKZ",
        "verified_at": "2025-06-10",
        "content": "L'IBAM propose des Licences Professionnelles en Comptabilité Contrôle Audit (CCA, accessible Bacs D, G1, G2), Informatique de Gestion (accessible Bacs C, D, E, G2), Méthodes Informatiques Appliquées à la Gestion (MIAGE) et Assistant de Direction."
    },
    {
        "doc_id": "BF_UTS_2026_IFOAD",
        "title": "Formations à Distance de l'IFOAD - Université Thomas Sankara (UTS)",
        "institution": "Université Thomas Sankara (UTS)",
        "source": "Catalogue Officiel IFOAD / UTS",
        "verified_at": "2026-01-13",
        "content": "L'IFOAD de l'Université Thomas Sankara offre des formations ouvertes à distance (FOAD) conformes au nouveau régime LMD : Développement Local et Gestion des collectivités (DEVLOG), Économie et Gestion des Entreprises d'Économie Sociale et Solidaire (EGEES), Analyse et Suivi-évaluation des Politiques."
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
        if any(term in doc["title"].lower() or term in doc["content"].lower() or term in doc["institution"].lower() for term in query_lower.split()):
            matched_docs.append(doc)

    if not matched_docs:
        matched_docs = INSTITUTIONAL_DOCUMENTS  # Fallback to general documents

    return {
        "query": query_text,
        "matched_documents_count": len(matched_docs),
        "documents": matched_docs,
        "disclaimer": "Informations documentaires officielles issues de la DGCOB, CampusFaso et des IESR du Burkina Faso."
    }
