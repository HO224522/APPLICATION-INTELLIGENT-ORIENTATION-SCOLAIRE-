from typing import Dict, Any, List
from app.db.database import get_db_connection
from app.services.llm_rag_service import sanitize_user_input, call_free_llm_explanation

def add_institutional_document(doc_id: str, title: str, institution: str, source: str, verified_at: str, content: str) -> Dict[str, Any]:
    """Ingests a verified institutional document into the persistent RAG database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (doc_id, title, institution, source, verified_at, content)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(doc_id) DO UPDATE SET
            title = excluded.title,
            institution = excluded.institution,
            source = excluded.source,
            verified_at = excluded.verified_at,
            content = excluded.content
    """, (doc_id, title, institution, source, verified_at, content))
    conn.commit()
    conn.close()
    return {"status": "success", "doc_id": doc_id, "title": title}

def query_persistent_rag_knowledge_base(query_text: str) -> Dict[str, Any]:
    """Searches persistent documents database for official information."""
    safe_query = sanitize_user_input(query_text).lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doc_id, title, institution, source, verified_at, content FROM documents")
    rows = cursor.fetchall()
    conn.close()

    matched_docs = []
    keywords = safe_query.split()
    for row in rows:
        title_l = row["title"].lower()
        content_l = row["content"].lower()
        inst_l = row["institution"].lower()
        if any(k in title_l or k in content_l or k in inst_l for k in keywords):
            matched_docs.append({
                "doc_id": row["doc_id"],
                "title": row["title"],
                "institution": row["institution"],
                "source": row["source"],
                "verified_at": row["verified_at"],
                "content": row["content"]
            })

    if not matched_docs and rows:
        # Fallback to all documents if specific match is empty
        matched_docs = [{
            "doc_id": r["doc_id"],
            "title": r["title"],
            "institution": r["institution"],
            "source": r["source"],
            "verified_at": r["verified_at"],
            "content": r["content"]
        } for r in rows[:3]]

    return {
        "query": query_text,
        "matched_documents_count": len(matched_docs),
        "documents": matched_docs,
        "disclaimer": "Informations documentaires officielles issues de la base de données de la DGCOB, CampusFaso et des universités du Burkina Faso."
    }

def handle_live_chat_query(user_message: str) -> Dict[str, Any]:
    """
    Live Assistant Pipeline:
    1. Sanitize user input.
    2. Query persistent RAG knowledge base.
    3. Generate natural answer using Free LLM / Local engine.
    """
    safe_msg = sanitize_user_input(user_message)
    rag_res = query_persistent_rag_knowledge_base(safe_msg)

    docs_summary = []
    for d in rag_res["documents"][:2]:
        docs_summary.append(f"Source: {d['title']} ({d['institution']}) - {d['content']}")

    prompt_struct = {
        "positive_factors": [f"Question posée : '{safe_msg}'"],
        "warning_factors": docs_summary if docs_summary else ["Aucun document directement spécifique mais voici les règles générales."]
    }

    bot_response = call_free_llm_explanation(prompt_struct)

    return {
        "user_message": safe_msg,
        "assistant_response": bot_response,
        "retrieved_sources": [d["title"] for d in rag_res["documents"][:2]]
    }
