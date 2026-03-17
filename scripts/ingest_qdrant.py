from qdrant_client.http.models import PointStruct
import uuid
import sys
import os
import pandas as pd

# Ensure the core_engine package is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_engine.datasets.database import qdrant, QDRANT_COLLECTION, init_qdrant
from core_engine.embedding_service import embedding_service

DATA_PATH = "core_engine/data_layer/raw/job_dataset.csv"

def ingest_data():
    print(f"DEBUG: Starting ingestion from {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"ERROR: Dataset not found at {DATA_PATH}")
        sys.exit(1)

    # Initialize Qdrant collection if it doesn't exist
    init_qdrant()

    # To keep ingestion fast for this prototype, we'll limit to first 1000 rows
    limit = 1000
    df = df.head(limit)
    print(f"DEBUG: Processing top {limit} job postings...")

    points = []
    
    for index, row in df.iterrows():
        # Clean data (handle NaNs)
        title = str(row.get('Title', 'Unknown Job'))
        skills = str(row.get('Skills', ''))
        responsibilities = str(row.get('Responsibilities', ''))
        
        # Combine text for embedding (same logic as search)
        text_to_embed = f"{title}. Skills: {skills}. Responsibilities: {responsibilities}"
        
        # Create an embedding using the shared service
        embedding = embedding_service.encode(text_to_embed).tolist()
        
        # Generate a unique ID (Qdrant expects string UUID or int)
        point_id = str(uuid.uuid4())
        
        # Prepare metadata payload
        payload = {
            "title": title,
            "skills": [s.strip() for s in skills.split(',') if s.strip()],
            "description": responsibilities,
            "experience_level": str(row.get('ExperienceLevel', 'Not specified')),
            "years_of_experience": str(row.get('YearsOfExperience', '0'))
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
