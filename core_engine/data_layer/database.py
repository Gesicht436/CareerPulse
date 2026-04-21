import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION = "job_descriptions"
VECTOR_SIZE = 384  # Dimension for all-MiniLM-L6-v2

# Initialize Qdrant Client
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def init_qdrant():
    """
    Ensures that the required collection exists in Qdrant with the correct vector configuration.
    """
    collections = qdrant.get_collections().collections
    exists = any(c.name == QDRANT_COLLECTION for c in collections)
    
    if not exists:
        qdrant.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Created Qdrant collection: {QDRANT_COLLECTION}")
    else:
        print(f"Qdrant collection '{QDRANT_COLLECTION}' already exists.")

if __name__ == "__main__":
    # Test initialization
    init_qdrant()
