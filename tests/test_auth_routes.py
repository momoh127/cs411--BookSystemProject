import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app
from utils.db_utils import reset_test_database
from utils.auth_utils import hash_password, verify_password

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask app.
    """
    with app.test_client() as client:
        yield client

def setup_module(module):
    """
    Reset the database before running tests.
    """
    reset_test_database()

def test_create_account(client):
    """
    Test the /auth/create-account route.
    """
    payload = {"username": "testuser", "password": "securepassword123"}
    response = client.post("/auth/create-account", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Account created successfully!"

def test_duplicate_account(client):
    """
    Test creating a duplicate account with the same username.
    """
    payload = {"username": "testuser", "password": "securepassword123"}
    response = client.post("/auth/create-account", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Username already exists."

def test_login_success(client):
    """
    Test successful login using /auth/login route.
    """
    payload = {"username": "testuser", "password": "securepassword123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Login successful!"

def test_login_failure(client):
    """
    Test login failure due to incorrect password.
    """
    payload = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid username or password."

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_auth_routes.py"])