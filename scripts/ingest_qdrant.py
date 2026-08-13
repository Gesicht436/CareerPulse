import uuid
import sys
import os
import pandas as pd

# Ensure the core_engine package is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_engine.data_layer.database import init_db, save_jobs
from core_engine.data_layer.schemas import JobDescriptionModel
from core_engine.data_layer.service import data_layer_service

DATA_PATH = "core_engine/datasets/raw/job_descriptions.csv"

def ingest_data():
    print(f"DEBUG: Starting ingestion from {DATA_PATH} into SQLite...")
    try:
        limit = 5000
        df = pd.read_csv(DATA_PATH, nrows=150000)
        step = max(1, len(df) // limit)
        sampled_df = df.iloc[::step].reset_index(drop=True)
    except FileNotFoundError:
        print(f"ERROR: Dataset not found at {DATA_PATH}")
        sys.exit(1)

    init_db()

    print(f"DEBUG: Processing top {len(sampled_df)} job postings...")

    jobs = []
    
    for index, row in sampled_df.iterrows():
        title = str(row.get('Job Title', '') or row.get('Role', 'Unknown Job')).strip()
        company = str(row.get('Company', 'Unknown Company')).strip()
        location = str(row.get('location', '')).strip()
        country = str(row.get('Country', '')).strip()
        skills = str(row.get('skills', '')).strip()
        description = str(row.get('Job Description', '')).strip()
        experience = str(row.get('Experience', '')).strip()
        qualifications = str(row.get('Qualifications', '')).strip()
        salary_range = str(row.get('Salary Range', '')).strip()
        work_type = str(row.get('Work Type', '')).strip()
        
        job_id = str(row.get('Job Id', f"job-{index+1}"))
        skills_list = [s.strip() for s in skills.split(',') if s.strip()]
        
        jobs.append(JobDescriptionModel(
            id=job_id,
            title=title,
            company=company,
            location=location,
            country=country,
            description=description,
            skills=skills_list,
            experience=experience,
            qualifications=qualifications,
            salary_range=salary_range,
            work_type=work_type
        ))

    save_jobs(jobs)
    print(f"SUCCESS: Saved {len(jobs)} jobs into SQLite database!")
    
    print("DEBUG: Generating PyTorch vector embeddings cache matrix...")
    data_layer_service._get_dataset_embeddings(jobs)
    print("SUCCESS: Vector embedding matrix pre-computed and cached!")

if __name__ == "__main__":
    ingest_data()
