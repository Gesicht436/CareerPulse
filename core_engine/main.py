from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---

@app.get("/health", tags=["Health"])
def health_check():
    """Returns the API health status."""
    return {
        "status": "online",
        "api_version": settings.API_VERSION,
        "debug_mode": settings.DEBUG
    }

@app.get("/test-db", tags=["Health"])
def test_db_connections():
    """Verifies connection to the vector engine."""
    try:
        # Check Qdrant connection
        qdrant = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        qdrant_status = qdrant.get_collections()
        return {
            "status": "connected",
            "qdrant_response": f"Found {len(qdrant_status.collections)} collections"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("core_engine.main:app", host="0.0.0.0", port=8000, reload=True)
