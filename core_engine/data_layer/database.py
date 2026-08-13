import sqlite3
import os
import json
from typing import List, Optional
from core_engine.data_layer.schemas import JobDescriptionModel

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "jobs.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Ensures that the required SQLite database and jobs table exist.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                country TEXT,
                description TEXT NOT NULL,
                skills TEXT,
                experience TEXT,
                qualifications TEXT,
                salary_range TEXT,
                work_type TEXT
            )
        """)
        conn.commit()
    print(f"DEBUG: SQLite database initialized at '{DB_PATH}'.")

def save_jobs(jobs: List[JobDescriptionModel]):
    """
    Inserts or updates a list of JobDescriptionModel items into SQLite.
    """
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        for job in jobs:
            cursor.execute("""
                INSERT OR REPLACE INTO jobs (
                    id, title, company, location, country, description,
                    skills, experience, qualifications, salary_range, work_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.id,
                job.title,
                job.company,
                job.location or "",
                job.country or "",
                job.description,
                json.dumps(job.skills or []),
                job.experience or "",
                job.qualifications or "",
                job.salary_range or "",
                job.work_type or ""
            ))
        conn.commit()
    print(f"DEBUG: Saved {len(jobs)} jobs to SQLite database.")

def fetch_all_jobs() -> List[JobDescriptionModel]:
    """
    Retrieves all jobs stored in SQLite database.
    """
    if not os.path.exists(DB_PATH):
        return []
    
    jobs = []
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        for row in rows:
            skills_raw = row["skills"]
            try:
                skills_list = json.loads(skills_raw) if skills_raw else []
            except Exception:
                skills_list = [s.strip() for s in str(skills_raw).split(",") if s.strip()]
            
            jobs.append(JobDescriptionModel(
                id=row["id"],
                title=row["title"],
                company=row["company"],
                location=row["location"],
                country=row["country"],
                description=row["description"],
                skills=skills_list,
                experience=row["experience"],
                qualifications=row["qualifications"],
                salary_range=row["salary_range"],
                work_type=row["work_type"]
            ))
    return jobs

def fetch_job_by_id(job_id: str) -> Optional[JobDescriptionModel]:
    """
    Retrieves a single job by its ID.
    """
    if not os.path.exists(DB_PATH):
        return None
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if not row:
            return None
        skills_raw = row["skills"]
        try:
            skills_list = json.loads(skills_raw) if skills_raw else []
        except Exception:
            skills_list = [s.strip() for s in str(skills_raw).split(",") if s.strip()]
        
        return JobDescriptionModel(
            id=row["id"],
            title=row["title"],
            company=row["company"],
            location=row["location"],
            country=row["country"],
            description=row["description"],
            skills=skills_list,
            experience=row["experience"],
            qualifications=row["qualifications"],
            salary_range=row["salary_range"],
            work_type=row["work_type"]
        )

if __name__ == "__main__":
    init_db()
