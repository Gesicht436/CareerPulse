import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from core_engine.main import app

client = TestClient(app)

def test_auth_flow():
    import time
    test_email = f"test_{int(time.time())}@example.com"
    test_password = "securepassword123"

    # 1. Signup
    signup_resp = client.post("/api/v1/auth/signup", json={
        "full_name": "Test Candidate",
        "email": test_email,
        "password": test_password
    })
    assert signup_resp.status_code == 200
    signup_data = signup_resp.json()
    assert "access_token" in signup_data
    assert signup_data["user"]["email"] == test_email

    token = signup_data["access_token"]

    # 2. Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data
    login_token = login_data["access_token"]

    # 3. Get Current User (/me)
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {login_token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == test_email
    assert me_data["full_name"] == "Test Candidate"
