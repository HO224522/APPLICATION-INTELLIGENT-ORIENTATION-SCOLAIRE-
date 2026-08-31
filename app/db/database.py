import os
import json
import sqlite3
from typing import Dict, Any, List, Optional
from app.models.schemas import StudentProfile, FieldProfile, FeedbackItem

DB_PATH = os.getenv("DATABASE_PATH", "orientation.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes SQLite production tables for persistent real data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            profile_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Fields table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            field_id TEXT PRIMARY KEY,
            field_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Feedbacks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recommendation_id TEXT NOT NULL,
            expert_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            suggested_field_id TEXT,
            reason TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Documents table for live RAG
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            institution TEXT NOT NULL,
            source TEXT NOT NULL,
            verified_at TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def seed_initial_data_if_empty():
    """Seeds official fields and institutional documents from initial json if DB is empty."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check fields
    cursor.execute("SELECT COUNT(*) as count FROM fields")
    if cursor.fetchone()["count"] == 0:
        fields_path = "data/synthetic/fields.json"
        if os.path.exists(fields_path):
            with open(fields_path, "r", encoding="utf-8") as f:
                fields_data = json.load(f)
                for item in fields_data:
                    cursor.execute(
                        "INSERT INTO fields (field_id, field_data) VALUES (?, ?)",
                        (item["field_id"], json.dumps(item, ensure_ascii=False))
                    )

    # Check students
    cursor.execute("SELECT COUNT(*) as count FROM students")
    if cursor.fetchone()["count"] == 0:
        students_path = "data/synthetic/students.json"
        if os.path.exists(students_path):
            with open(students_path, "r", encoding="utf-8") as f:
                students_data = json.load(f)
                for item in students_data:
                    cursor.execute(
                        "INSERT INTO students (student_id, profile_data) VALUES (?, ?)",
                        (item["student_id"], json.dumps(item, ensure_ascii=False))
                    )

    # Check documents
    cursor.execute("SELECT COUNT(*) as count FROM documents")
    if cursor.fetchone()["count"] == 0:
        from app.rag.knowledge_base import INSTITUTIONAL_DOCUMENTS
        for doc in INSTITUTIONAL_DOCUMENTS:
            cursor.execute(
                "INSERT INTO documents (doc_id, title, institution, source, verified_at, content) VALUES (?, ?, ?, ?, ?, ?)",
                (doc["doc_id"], doc["title"], doc["institution"], doc["source"], doc["verified_at"], doc["content"])
            )

    conn.commit()
    conn.close()
