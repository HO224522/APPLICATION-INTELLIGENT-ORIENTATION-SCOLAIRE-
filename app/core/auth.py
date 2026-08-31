import os
import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Any, Optional

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "BURKINA_FASO_GUIDANCE_SECURE_JWT_SECRET_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600 * 8  # 8 hours token validity

def hash_password(password: str) -> str:
    """Hashes user password using PBKDF2-HMAC-SHA256 (Cybersecurity Standard)."""
    salt = "BF_ORIENTATION_SALT_2026".encode('utf-8')
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain password against stored hash."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def _b64_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(user_id: str, role: str, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    """
    Creates signed JWT token with user_id, role (student, parent, counselor, admin) and expiration.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "role": role,
        "exp": int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS,
        "iat": int(time.time())
    }
    if extra_claims:
        payload.update(extra_claims)

    header_b64 = _b64_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = _b64_encode(json.dumps(payload).encode('utf-8'))

    signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
    signature_b64 = _b64_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodes and verifies JWT token signature and expiration.
    """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Token JWT malformé.")

        header_b64, payload_b64, signature_b64 = parts
        signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()

        if not hmac.compare_digest(_b64_encode(expected_sig), signature_b64):
            raise ValueError("Signature du jeton JWT invalide.")

        payload = json.loads(_b64_decode(payload_b64).decode('utf-8'))
        if payload.get("exp", 0) < int(time.time()):
            raise ValueError("Jeton JWT expiré.")

        return payload
    except Exception as e:
        raise ValueError(f"Erreur d'authentification : {str(e)}")
