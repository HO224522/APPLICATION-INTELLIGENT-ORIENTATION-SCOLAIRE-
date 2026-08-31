import os
import re
import json
import urllib.request
from typing import Dict, Any, List

def sanitize_user_input(text: str) -> str:
    """Cybersecurity input sanitization against prompt injection & XSS."""
    if not text:
        return ""
    sanitized = re.sub(r'(?i)(ignore previous instructions|system prompt|override rules|forget your instructions)', '[REDACTED]', text)
    sanitized = re.sub(r'<[^>]*>', '', sanitized)
    return sanitized.strip()

def compute_local_text_embedding(text: str) -> List[float]:
    clean = sanitize_user_input(text).lower()
    words = re.findall(r'\w+', clean)
    vector = [0.0] * 64
    for w in words:
        idx = hash(w) % 64
        vector[idx] += 1.0
    norm = sum(v*v for v in vector) ** 0.5
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector

def call_free_llm_explanation(structured_explanation: Dict[str, Any], lang: str = "fr") -> str:
    """
    Generates natural, fluid, professional French responses.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.1-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un conseiller d'orientation scolaire d'élite au Burkina Faso. Réponds de façon naturelle, synthétique, fluide et très professionnelle en français. Ne montre jamais de structures brutes JSON."
                    },
                    {
                        "role": "user",
                        "content": f"Information : {json.dumps(structured_explanation, ensure_ascii=False)}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 400
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data["choices"][0]["message"]["content"]
        except Exception:
            pass

    # High-quality Deterministic Natural Language Formatter (0 FCFA, 100% reliable)
    positives = structured_explanation.get("positive_factors", [])
    warnings = structured_explanation.get("warning_factors", [])
    violations = structured_explanation.get("hard_constraints_violated", [])

    parts = []
    if positives:
        parts.append("✅ **Atouts et points forts identifiés :**\n" + "\n".join([f"• {p}" for p in positives]))
    if warnings:
        parts.append("⚠️ **Points de vigilance à prendre en compte :**\n" + "\n".join([f"• {w}" for w in warnings]))
    if violations:
        parts.append("❌ **Contraintes administratives :**\n" + "\n".join([f"• {v}" for v in violations]))

    return "\n\n".join(parts) if parts else "Analyse terminée sans observation particulière."
