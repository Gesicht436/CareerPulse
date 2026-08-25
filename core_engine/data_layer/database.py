import sqlite3
import os
import json
from typing import List, Optional, Dict, Any
from core_engine.data_layer.schemas import JobDescriptionModel

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "jobs.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable WAL mode and optimized cache for high concurrency & speed
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn

def init_db():
    """
    Ensures that the required SQLite database and jobs table exist with the full schema.
    Applies column migrations if upgrading from an older schema.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                role TEXT,
                company TEXT NOT NULL,
                location TEXT,
                country TEXT,
                work_type TEXT,
                experience INTEGER,
                qualifications TEXT,
                salary_range TEXT,
                skills TEXT,
                responsibilities TEXT,
                description TEXT NOT NULL,
                job_portal TEXT,
                preference TEXT,
                contact_person TEXT,
                contact TEXT,
                company_profile TEXT
            )
        """)
        
        # Check and migrate columns if upgrading from legacy schema
        cursor.execute("PRAGMA table_info(jobs)")
        existing_cols = {row["name"] for row in cursor.fetchall()}
        
        needed_cols = {
            "role": "TEXT",
            "responsibilities": "TEXT",
            "job_portal": "TEXT",
            "preference": "TEXT",
            "contact_person": "TEXT",
            "contact": "TEXT",
            "company_profile": "TEXT"
        }
        
        for col_name, col_type in needed_cols.items():
            if col_name not in existing_cols:
                cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col_name} {col_type}")

        # Index on qualifications and role for high-speed filtered queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_qual ON jobs (qualifications)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_role ON jobs (role)")
        conn.commit()
    print(f"DEBUG: SQLite database initialized at '{DB_PATH}'.")

def save_jobs(jobs: List[JobDescriptionModel]):
    """
    Inserts or updates a list of JobDescriptionModel items into SQLite in a single transaction.
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        rows_to_insert = []
        for job in jobs:
            skills_json = json.dumps(job.skills or []) if isinstance(job.skills, list) else str(job.skills or "")
            profile_json = json.dumps(job.company_profile or {}) if isinstance(job.company_profile, dict) else str(job.company_profile or "")
            exp_val = int(job.experience) if job.experience is not None and str(job.experience).isdigit() else None
            
            rows_to_insert.append((
                job.id,
                job.title,
                job.role or "",
                job.company,
                job.location or "",
                job.country or "",
                job.work_type or "",
                exp_val,
                job.qualifications or "",
                job.salary_range or "",
                skills_json,
                job.responsibilities or "",
                job.description,
                job.job_portal or "",
                job.preference or "",
                job.contact_person or "",
                job.contact or "",
                profile_json
            ))

        cursor.executemany("""
            INSERT OR REPLACE INTO jobs (
                id, title, role, company, location, country, work_type,
                experience, qualifications, salary_range, skills,
                responsibilities, description, job_portal, preference,
                contact_person, contact, company_profile
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rows_to_insert)
        conn.commit()
    print(f"DEBUG: Saved {len(jobs)} jobs to SQLite database.")

def _row_to_model(row: sqlite3.Row) -> JobDescriptionModel:
    skills_raw = row["skills"]
    try:
        skills_list = json.loads(skills_raw) if skills_raw else []
        if not isinstance(skills_list, list):
            skills_list = [s.strip() for s in str(skills_raw).split(",") if s.strip()]
    except Exception:
        skills_list = [s.strip() for s in str(skills_raw).split(",") if s.strip()]

    profile_raw = row["company_profile"] if "company_profile" in row.keys() else "{}"
    try:
        profile_dict = json.loads(profile_raw) if profile_raw else {}
    except Exception:
        profile_dict = {}

    return JobDescriptionModel(
        id=str(row["id"]),
        title=row["title"],
        role=row["role"] if "role" in row.keys() and row["role"] else row["title"],
        company=row["company"],
        location=row["location"],
        country=row["country"],
        work_type=row["work_type"] if "work_type" in row.keys() else "",
        experience=row["experience"] if "experience" in row.keys() else None,
        qualifications=row["qualifications"],
        salary_range=row["salary_range"],
        skills=skills_list,
        responsibilities=row["responsibilities"] if "responsibilities" in row.keys() else "",
        description=row["description"],
        job_portal=row["job_portal"] if "job_portal" in row.keys() else "",
        preference=row["preference"] if "preference" in row.keys() else "",
        contact_person=row["contact_person"] if "contact_person" in row.keys() else "",
        contact=row["contact"] if "contact" in row.keys() else "",
        company_profile=profile_dict
    )

def fetch_all_jobs() -> List[JobDescriptionModel]:
    """
    Retrieves all jobs stored in SQLite database.
    """
    if not os.path.exists(DB_PATH):
        return []
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        return [_row_to_model(row) for row in rows]

def fetch_job_by_id(job_id: str) -> Optional[JobDescriptionModel]:
    """
    Retrieves a single job by its ID.
    """
    if not os.path.exists(DB_PATH):
        return None
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (str(job_id),))
        row = cursor.fetchone()
        if not row:
            return None
        return _row_to_model(row)

def fetch_jobs_by_ids(job_ids: List[str]) -> List[JobDescriptionModel]:
    """
    High-speed batch retrieval for specific job IDs using primary key index.
    """
    if not os.path.exists(DB_PATH) or not job_ids:
        return []
    
    placeholders = ",".join("?" for _ in job_ids)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM jobs WHERE id IN ({placeholders})", [str(jid) for jid in job_ids])
        rows = cursor.fetchall()
        
        # Maintain original order of job_ids
        row_dict = {str(row["id"]): _row_to_model(row) for row in rows}
        return [row_dict[str(jid)] for jid in job_ids if str(jid) in row_dict]

if __name__ == "__main__":
    init_db()
