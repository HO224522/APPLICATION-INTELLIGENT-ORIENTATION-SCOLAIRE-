import hashlib
from typing import Dict, Any

def anonymize_student_id(raw_id: str, salt: str = "BF_GUIDANCE_2025") -> str:
    """Hashes student identifier to comply with minor data privacy regulations."""
    return hashlib.sha256(f"{salt}_{raw_id}".encode('utf-8')).hexdigest()[:16]

def sanitize_profile_for_audit(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Removes sensitive personal identifiers while retaining attributes needed for bias auditing."""
    sanitized = profile_data.copy()
    sensitive_keys = ["first_name", "last_name", "phone", "email", "address", "parent_contact"]
    for key in sensitive_keys:
        sanitized.pop(key, None)
    return sanitized
