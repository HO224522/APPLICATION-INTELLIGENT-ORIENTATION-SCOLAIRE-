from typing import Dict, Any, List
from app.db.database import get_db_connection
from app.services.llm_rag_service import sanitize_user_input, call_free_llm_explanation

def query_persistent_rag_knowledge_base(query_text: str) -> Dict[str, Any]:
    safe_query = sanitize_user_input(query_text).lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doc_id, title, institution, source, verified_at, content FROM documents")
    rows = cursor.fetchall()
    conn.close()

    matched_docs = []
    keywords = [k for k in safe_query.split() if len(k) > 2]

    for row in rows:
        title_l = row["title"].lower()
        content_l = row["content"].lower()
        inst_l = row["institution"].lower()
        # Score relevance by keyword hits
        score = sum(1 for k in keywords if k in title_l or k in content_l or k in inst_l)
        if score > 0:
            matched_docs.append((score, {
                "doc_id": row["doc_id"],
                "title": row["title"],
                "institution": row["institution"],
                "source": row["source"],
                "verified_at": row["verified_at"],
                "content": row["content"]
            }))

    matched_docs.sort(key=lambda x: x[0], reverse=True)
    results = [doc for score, doc in matched_docs]

    if not results and rows:
        results = [{
            "doc_id": r["doc_id"],
            "title": r["title"],
            "institution": r["institution"],
            "source": r["source"],
            "verified_at": r["verified_at"],
            "content": r["content"]
        } for r in rows[:2]]

    return {
        "query": query_text,
        "matched_documents_count": len(results),
        "documents": results,
        "disclaimer": "Informations documentaires officielles de la DGCOB, CampusFaso et des universités du Burkina Faso."
    }

def handle_live_chat_query(user_message: str) -> Dict[str, Any]:
    safe_msg = sanitize_user_input(user_message)
    rag_res = query_persistent_rag_knowledge_base(safe_msg)

    docs = rag_res["documents"]

    # Topic-specific conversational assistant response synthesis
    msg_l = safe_msg.lower()

    if "bourse" in msg_l or "dgcob" in msg_l or "ciospb" in msg_l or "cnbes" in msg_l:
        response_text = (
            "🎓 **Critères d'Éligibilité aux Bourses d'Études de la DGCOB (ex-CIOSPB) :**\n\n"
            "Pour bénéficier d'une bourse nationale de 1er cycle au Burkina Faso, la Commission Nationale (CNBES) exige :\n"
            "1. **Âge** : Avoir moins de 22 ans au moment de la demande de Licence 1.\n"
            "2. **Mérite Académique** : Obtenir une moyenne générale supérieure ou égale à **12.00/20** au Baccalauréat.\n"
            "3. **Situation Sociale** : Évaluation de la situation socio-économique du candidat.\n\n"
            "📌 *Les demandes s'effectuent en ligne lors des sessions de la DGCOB sur le portail www.ciospb.gov.bf.*"
        )
    elif "université" in msg_l or "meilleur" in msg_l or "iesr" in msg_l or "école" in msg_l:
        response_text = (
            "🏛️ **Institutions d'Enseignement Supérieur Majeures au Burkina Faso :**\n\n"
            "La nouvelle carte universitaire du MESRI classe les établissements en deux catégories :\n"
            "• **Universités Généralistes** : Université Joseph Ki-Zerbo (UJKZ - Ouaga), Université Nazi Boni (UNB - Bobo), "
            "Université Norbert Zongo (UNZ - Koudougou) et l'Université Virtuelle du Burkina Faso (UV-BF).\n"
            "• **Grandes Écoles & Instituts Spécialisés** : École Polytechnique de Ouagadougou (EPO / CPGE), "
            "Université Thomas Sankara (UTS - Droit/Économie), ISGE-BF et IBAM.\n\n"
            "💡 *Le choix de la 'meilleure' université dépend avant tout de votre série de BAC et de la filière visée.*"
        )
    elif "campusfaso" in msg_l or "inscription" in msg_l or "orientation" in msg_l:
        response_text = (
            "💻 **Procédure d'Orientation Officielle CampusFaso :**\n\n"
            "Toutes les demandes d'orientation post-BAC dans le public et le privé conventionné s'effectuent sur **www.campusfaso.bf**.\n"
            "• Vous formulez vos vœux par ordre de préférence.\n"
            "• L'affectation est automatique selon la moyenne au BAC et les notes obtenues dans les matières clés de la filière."
        )
    else:
        # General response synthesis from top retrieved RAG document
        top_doc = docs[0] if docs else None
        if top_doc:
            response_text = (
                f"ℹ️ **Informations d'Orientation Officielle ({top_doc['institution']}) :**\n\n"
                f"{top_doc['content']}\n\n"
                f"📌 *Source vérifiée : {top_doc['source']} ({top_doc['verified_at']})*"
            )
        else:
            response_text = "Je suis à votre disposition pour vous renseigner sur les filières, les bourses de la DGCOB et les procédures CampusFaso au Burkina Faso."

    return {
        "user_message": safe_msg,
        "assistant_response": response_text,
        "retrieved_sources": [d["title"] for d in docs[:2]]
    }
