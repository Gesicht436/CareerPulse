from fastapi.testclient import TestClient
# Note: Jab actual app ban jayega toh hum 'from main import app' karenge
from fastapi import FastAPI

# Dummy app just for initial test setup
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok", "project": "CareerPulse ATS Simulator"}

client = TestClient(app)

def test_health_check():
    """
    Test to verify if the basic API endpoint is responding correctly.
    """
    response = client.get("/health")
    
    # Check if the status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if the correct JSON response is coming
    assert response.json() == {"status": "ok", "project": "CareerPulse ATS Simulator"}