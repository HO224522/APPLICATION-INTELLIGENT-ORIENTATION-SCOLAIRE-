import json
from typing import List, Optional
from app.db.database import get_db_connection
from app.models.schemas import StudentProfile

def save_student_profile(profile: StudentProfile) -> StudentProfile:
    """Saves or updates a real student profile in the persistent database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    data_str = json.dumps(profile.model_dump(), ensure_ascii=False)

    cursor.execute("""
        INSERT INTO students (student_id, profile_data)
        VALUES (?, ?)
        ON CONFLICT(student_id) DO UPDATE SET profile_data = excluded.profile_data
    """, (profile.student_id, data_str))

    conn.commit()
    conn.close()
    return profile

def get_student_profile_by_id(student_id: str) -> Optional[StudentProfile]:
    """Retrieves a persistent student profile by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT profile_data FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None
    return StudentProfile(**json.loads(row["profile_data"]))

def list_all_student_profiles() -> List[StudentProfile]:
    """Lists all stored student profiles."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT profile_data FROM students")
    rows = cursor.fetchall()
    conn.close()

    return [StudentProfile(**json.loads(row["profile_data"])) for row in rows]
