import os
import re
import json
import urllib.request
from typing import Dict, Any, List

def sanitize_user_input(text: str) -> str:
    """
    Cybersecurity input sanitization:
    Mitigates Prompt Injection attacks and strips malicious control characters or script injections.
    """
    if not text:
        return ""
    # Strip potential prompt injection overrides
    sanitized = re.sub(r'(?i)(ignore previous instructions|system prompt|override rules|forget your instructions)', '[REDACTED]', text)
    # Remove HTML/Script tags
    sanitized = re.sub(r'<[^>]*>', '', sanitized)
    return sanitized.strip()

def compute_local_text_embedding(text: str) -> List[float]:
    """
    Computes text embedding using 100% FREE local lightweight algorithm
    (Term Frequency + Normalized Hashing vectorizer), avoiding paid OpenAI/Cohere embedding APIs.
    """
    clean = sanitize_user_input(text).lower()
    words = re.findall(r'\w+', clean)
    vector = [0.0] * 64
    for w in words:
        idx = hash(w) % 64
        vector[idx] += 1.0
    # L2 Normalization
    norm = sum(v*v for v in vector) ** 0.5
    if norm > 0:
        vector = [v / norm for v in vector]
    return vector

def call_free_llm_explanation(structured_explanation: Dict[str, Any], lang: str = "fr") -> str:
    """
    Generates natural language explanation from structured recommendation output.
    Attempts Free Provider 1: Groq API (Free Tier),
    Fallback Provider 2: Ollama Local Server (http://localhost:11434),
    Fallback Provider 3: Deterministic Rule-Based Formatter (100% offline, 0 FCFA, 100% secure).
    """
    # 1. Try Groq API if GROQ_API_KEY is available
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.1-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un conseiller d'orientation scolaire bienveillant au Burkina Faso. Synthétise l'explication basée STRICTEMENT sur les données fournies sans en inventer."
                    },
                    {
                        "role": "user",
                        "content": f"Données d'explication : {json.dumps(structured_explanation, ensure_ascii=False)}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 300
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
            pass  # Fallback to local / rule-based format

    # 2. Try Ollama local endpoint if available
    try:
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        payload = {
            "model": "llama3.2:3b",
            "prompt": f"Synthétise en français pour un élève burkinabè : {json.dumps(structured_explanation, ensure_ascii=False)}",
            "stream": False
        }
        req = urllib.request.Request(
            ollama_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("response", "")
    except Exception:
        pass

    # 3. Deterministic Secure Fallback (0 FCFA, 100% robust, 0 hallucination)
    positives = structured_explanation.get("positive_factors", [])
    warnings = structured_explanation.get("warning_factors", [])
    violations = structured_explanation.get("hard_constraints_violated", [])

    lines = ["Analyse d'orientation :"]
    if positives:
        lines.append("\nPoints forts :")
        lines.extend([f"  • {p}" for p in positives])
    if warnings:
        lines.append("\nPoints de vigilance :")
        lines.extend([f"  • {w}" for w in warnings])
    if violations:
        lines.append("\nInéligibilité administrative :")
        lines.extend([f"  • {v}" for v in violations])

    return "\n".join(lines)
