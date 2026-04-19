import pytest
from fastapi.testclient import TestClient
import sys
import os

# Raasta dikhane ke liye
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_simple_check():
    # Ye bas check karne ke liye ki pytest chal raha hai
    assert 1 + 1 == 2

def test_app_import():
    # Isse pata chal jayega ki app import ho raha hai ya nahi
    from core_engine.main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200