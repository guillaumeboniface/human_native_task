import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.mock_db import db

# Create a test client
client = TestClient(app)

# Test data
VALID_API_KEY = "test_api_key"
INVALID_API_KEY = "invalid_api_key"
VALID_VIOLATION = {
    "dataset_id": "dataset_123",
    "item_id": "item_123",
    "jurisdictions": ["us", "eu"],
    "type": "privacy"
}
INVALID_VIOLATION = {
    "dataset_id": "",  # Invalid: empty string
    "item_id": "item_123",
    "jurisdictions": [],  # Invalid: empty list
    "type": "invalid_type"  # Invalid: not in enum
}

@pytest.fixture(autouse=True)
def setup_database():
    # Setup: Add test API key and dataset item
    db.api_keys.update(
        {
            VALID_API_KEY: {
                "id": "user_123",
                "customer_id": "customer_123"
            }
        }
    )
    db.dataset_items.add(("dataset_123", "item_123"))
    yield
    # Teardown: Clean up test data
    db.api_keys.clear()
    db.dataset_items.clear()

def test_create_violation_success():
    """Test successful violation creation"""
    response = client.post(
        "/violation",
        json=VALID_VIOLATION,
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "id" in data["data"]  # Check if UUID was added

def test_create_violation_invalid_api_key():
    """Test violation creation with invalid API key"""
    response = client.post(
        "/violation",
        json=VALID_VIOLATION,
        headers={"X-API-Key": INVALID_API_KEY}
    )
    
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]

def test_create_violation_validation_error():
    """Test violation creation with invalid data"""
    response = client.post(
        "/violation",
        json=INVALID_VIOLATION,
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert len(data["detail"]) > 0

def test_create_violation_nonexistent_dataset():
    """Test violation creation for non-existent dataset item"""
    violation = VALID_VIOLATION.copy()
    violation["dataset_id"] = "nonexistent_dataset"
    
    response = client.post(
        "/violation",
        json=violation,
        headers={"X-API-Key": VALID_API_KEY}
    )
    
    assert response.status_code == 400
