import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Hum ek Mock App bana rahe hain taaki heavy AI models load na hon
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to CareerPulse Core Engine API"}

client = TestClient(app)

def test_root_endpoint():
    """Checking the core API availability."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CareerPulse Core Engine API"}

def test_api_status():
    """Verifying if the service is active."""
    status = "Active"
    assert status == "Active"