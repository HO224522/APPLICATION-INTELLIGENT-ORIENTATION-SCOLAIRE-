import json
from typing import List, Optional
from app.db.database import get_db_connection
from app.models.schemas import FieldProfile

def save_field_profile(field: FieldProfile) -> FieldProfile:
    """Saves or updates a candidate study field in the persistent database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    data_str = json.dumps(field.model_dump(), ensure_ascii=False)

    cursor.execute("""
        INSERT INTO fields (field_id, field_data)
        VALUES (?, ?)
        ON CONFLICT(field_id) DO UPDATE SET field_data = excluded.field_data
    """, (field.field_id, data_str))

    conn.commit()
    conn.close()
    return field

def get_field_profile_by_id(field_id: str) -> Optional[FieldProfile]:
    """Retrieves field profile by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT field_data FROM fields WHERE field_id = ?", (field_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None
    return FieldProfile(**json.loads(row["field_data"]))

def list_all_fields() -> List[FieldProfile]:
    """Lists all active study field profiles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT field_data FROM fields")
    rows = cursor.fetchall()
    conn.close()

    return [FieldProfile(**json.loads(row["field_data"])) for row in rows]
