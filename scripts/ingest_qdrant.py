from qdrant_client.http.models import PointStruct
import uuid
import sys
import os
import pandas as pd

# Ensure the core_engine package is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_engine.data_layer.database import qdrant, QDRANT_COLLECTION, init_qdrant
from core_engine.embedding_service import embedding_service

DATA_PATH = "core_engine/datasets/raw/job_descriptions.csv"

def ingest_data():
    print(f"DEBUG: Starting ingestion from {DATA_PATH}...")
    try:
        # The file is large, but we only read a portion if we use nrows
        limit = 1000
        df = pd.read_csv(DATA_PATH, nrows=limit)
    except FileNotFoundError:
        print(f"ERROR: Dataset not found at {DATA_PATH}")
        sys.exit(1)

    # Initialize Qdrant collection if it doesn't exist
    init_qdrant()

    print(f"DEBUG: Processing top {len(df)} job postings...")

    points = []
    
    for index, row in df.iterrows():
        # Clean data (handle NaNs) - Use new column names
        title = str(row.get('Job Title', 'Unknown Job'))
        company = str(row.get('Company', 'Unknown Company'))
        location = str(row.get('location', ''))
        country = str(row.get('Country', ''))
        skills = str(row.get('skills', ''))
        description = str(row.get('Job Description', ''))
        experience = str(row.get('Experience', ''))
        qualifications = str(row.get('Qualifications', ''))
        salary_range = str(row.get('Salary Range', ''))
        work_type = str(row.get('Work Type', ''))
        
        # Combine text for embedding
        text_to_embed = f"{title} at {company}. Location: {location}, {country}. Skills: {skills}. Description: {description}. Experience: {experience}. Qualifications: {qualifications}"
        
        # Create an embedding using the shared service
        embedding = embedding_service.encode(text_to_embed).tolist()
        
        # Generate a unique ID (Qdrant expects string UUID or int)
        point_id = str(uuid.uuid4())
        
        # Prepare metadata payload matching JobDescriptionModel
        payload = {
            "title": title,
            "company": company,
            "location": location,
            "country": country,
            "skills": [s.strip() for s in skills.split(',') if s.strip()],
            "description": description,
            "experience": experience,
            "qualifications": qualifications,
            "salary_range": salary_range,
            "work_type": work_type
        }
        
        # Create Point
        points.append(PointStruct(id=point_id, vector=embedding, payload=payload))
        
        if (index + 1) % 100 == 0:
            print(f"DEBUG: Processed {index + 1} rows...")

    print(f"DEBUG: Uploading {len(points)} points to Qdrant collection '{QDRANT_COLLECTION}'...")
    
    # Batch upload points
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        qdrant.upsert(
            collection_name=QDRANT_COLLECTION,
            points=batch
        )
        print(f"DEBUG: Uploaded batch {i//batch_size + 1} / {(len(points) + batch_size - 1) // batch_size}")

    print("SUCCESS: Data ingestion completed!")

if __name__ == "__main__":
    ingest_data()
