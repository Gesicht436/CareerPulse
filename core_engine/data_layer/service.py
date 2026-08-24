import os
import re
import pandas as pd
import torch
from typing import List, Dict, Any, Optional
from core_engine.data_layer.database import init_db, save_jobs, fetch_all_jobs
from core_engine.data_layer.schemas import JobDescriptionModel
from core_engine.embedding_service import embedding_service
from sentence_transformers import util

DATASET_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "raw", "job_descriptions.csv")
EMBEDDINGS_CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "dataset_embeddings_cache.pt")

DEGREE_GROUPS = {
    "engineering": ["b.tech", "b.e", "m.tech", "bca", "mca", "engineering", "computer science", "bachelor", "b.sc"],
    "science": ["b.sc", "m.sc", "ph.d", "phd", "science", "mathematics", "physics", "bachelor", "master"],
    "business": ["b.com", "mba", "bba", "m.com", "business", "finance", "accounting", "marketing", "management"],
    "general": ["bachelor", "master", "degree", "diploma", "graduate"]
}

class DataLayerService:
    def __init__(self):
        self._cached_dataset_jobs: Optional[List[JobDescriptionModel]] = None
        self._cached_dataset_embeddings: Optional[Any] = None

    def _load_real_dataset_jobs(self, target_sample_size: int = 5000) -> List[JobDescriptionModel]:
        """
        Dynamically loads real job descriptions from local SQLite store, 
        or populates SQLite from raw CSV if database is unseeded.
        """
        if self._cached_dataset_jobs is not None:
            return self._cached_dataset_jobs

        # 1. Try loading from SQLite database first
        jobs = fetch_all_jobs()
        if jobs:
            print(f"DEBUG: Successfully loaded {len(jobs)} jobs from local SQLite database.")
            self._cached_dataset_jobs = jobs
            return jobs

        # 2. Seed SQLite database from CSV if empty
        print(f"DEBUG: SQLite database empty. Initializing and parsing dataset from '{DATASET_CSV_PATH}'...")
        jobs = []
        if not os.path.exists(DATASET_CSV_PATH):
            raise FileNotFoundError(
                f"Job database 'jobs.db' is empty and dataset CSV was not found at '{DATASET_CSV_PATH}'. "
                "Please run 'python scripts/setup_data.py' and 'python scripts/ingest_qdrant.py' to initialize the database."
            )

        try:
            chunk_df = pd.read_csv(DATASET_CSV_PATH, nrows=150000)
            step = max(1, len(chunk_df) // target_sample_size)
            sampled_df = chunk_df.iloc[::step].reset_index(drop=True)

            for idx, row in sampled_df.iterrows():
                title = str(row.get('Job Title', '') or row.get('Role', 'Software Engineer')).strip()
                company = str(row.get('Company', 'Tech Company')).strip()
                location = str(row.get('location', 'Remote')).strip()
                country = str(row.get('Country', 'Global')).strip()
                desc = str(row.get('Job Description', '') or row.get('Responsibilities', '')).strip()
                exp = str(row.get('Experience', 'Not specified')).strip()
                qual = str(row.get('Qualifications', 'Degree in relevant field')).strip()
                salary = str(row.get('Salary Range', 'Industry standard')).strip()
                work_type = str(row.get('Work Type', 'Full-time')).strip()
                
                raw_skills = str(row.get('skills', ''))
                skills_list = [s.strip() for s in raw_skills.split(',') if s.strip()]
                job_id = str(row.get('Job Id', f"csv-{idx+1}"))

                jobs.append(JobDescriptionModel(
                    id=job_id,
                    title=title,
                    company=company,
                    location=location,
                    country=country,
                    description=desc,
                    skills=skills_list,
                    experience=exp,
                    qualifications=qual,
                    salary_range=salary,
                    work_type=work_type
                ))

            save_jobs(jobs)
            self._cached_dataset_jobs = jobs
            print(f"DEBUG: Successfully indexed and saved {len(jobs)} job postings into SQLite.")
        except Exception as e:
            print(f"ERROR reading job_descriptions.csv: {e}")
            raise RuntimeError(f"Failed to parse and seed job database from '{DATASET_CSV_PATH}': {str(e)}") from e

        return self._cached_dataset_jobs

    def _get_dataset_embeddings(self, jobs: List[JobDescriptionModel]):
        """
        Pre-computes and caches vector embeddings on disk/memory for sub-millisecond ranking.
        """
        if self._cached_dataset_embeddings is not None and len(self._cached_dataset_embeddings) == len(jobs):
            return self._cached_dataset_embeddings

        if os.path.exists(EMBEDDINGS_CACHE_PATH):
            try:
                print(f"DEBUG: Loading pre-computed embeddings matrix from '{EMBEDDINGS_CACHE_PATH}'...")
                self._cached_dataset_embeddings = torch.load(EMBEDDINGS_CACHE_PATH, weights_only=False)
                if len(self._cached_dataset_embeddings) == len(jobs):
                    return self._cached_dataset_embeddings
            except Exception as e:
                print(f"DEBUG: Cache load warning: {e}")

        print(f"DEBUG: Pre-computing vector embeddings for {len(jobs)} dataset job descriptions...")
        job_texts = [
            f"Role: {j.title}. Qualifications: {j.qualifications}. Skills: {', '.join(j.skills)}. Description: {j.description[:300]}"
            for j in jobs
        ]
        self._cached_dataset_embeddings = embedding_service.encode(job_texts, batch_size=64)
        try:
            torch.save(self._cached_dataset_embeddings, EMBEDDINGS_CACHE_PATH)
            print(f"DEBUG: Saved embeddings cache matrix to '{EMBEDDINGS_CACHE_PATH}'.")
        except Exception as e:
            print(f"DEBUG: Could not save cache matrix: {e}")

        return self._cached_dataset_embeddings

    def search_jobs(
        self, 
        query_text: str, 
        limit: int = 5, 
        experience_level: str = None,
        qualification: str = None,
        strict_qualification: bool = True
    ) -> List[JobDescriptionModel]:
        """
        Dynamically scans vector space using Section-Aware Weighted Vector Embedding Ranking.
        If strict_qualification=True, filters jobs matching the candidate's educational degree.
        """
        headline_query = query_text[:400]
        query_embs = embedding_service.encode([headline_query, query_text], batch_size=2)
        query_headline_emb = query_embs[0]
        query_full_emb = query_embs[1]

        dataset_jobs = self._load_real_dataset_jobs()
        if not dataset_jobs:
            raise RuntimeError("Job dataset is empty. Please verify database initialization.")

        # Filter candidate jobs by educational qualification if strict_qualification=True
        candidate_jobs = dataset_jobs
        candidate_indices = list(range(len(dataset_jobs)))

        if strict_qualification and qualification:
            qual_lower = qualification.lower().strip()
            filtered_pairs = []

            for idx, job in enumerate(dataset_jobs):
                job_qual_lower = (job.qualifications or "").lower() + " " + (job.description or "").lower() + " " + (job.title or "").lower()
                
                # Direct degree string match or degree group match
                if qual_lower in job_qual_lower:
                    filtered_pairs.append((idx, job))
                else:
                    # Match degree group keywords
                    matched_group = False
                    for group_name, keywords in DEGREE_GROUPS.items():
                        if any(k in qual_lower for k in keywords):
                            if any(k in job_qual_lower for k in keywords):
                                matched_group = True
                                break
                    if matched_group:
                        filtered_pairs.append((idx, job))

            if filtered_pairs:
                candidate_indices = [idx for idx, _ in filtered_pairs]
                candidate_jobs = [job for _, job in filtered_pairs]
                print(f"DEBUG: Educational Qualification Filter ACTIVE ('{qualification}'): Retained {len(candidate_jobs)} matching jobs.")
            else:
                raise ValueError(f"No job descriptions matching qualification '{qualification}' were found in the database.")

        dataset_embeddings = self._get_dataset_embeddings(dataset_jobs)
        filtered_embeddings = dataset_embeddings[candidate_indices]

        # Hybrid Section-Aware Weighting
        sim_headline = util.cos_sim(query_headline_emb, filtered_embeddings)[0]
        sim_full = util.cos_sim(query_full_emb, filtered_embeddings)[0]
        
        blended_sims = (0.40 * sim_headline) + (0.60 * sim_full)
        
        top_k_indices = torch.topk(blended_sims, k=min(limit, len(candidate_jobs))).indices.tolist()
        return [candidate_jobs[i] for i in top_k_indices]

data_layer_service = DataLayerService()
