import uuid
from typing import Optional
from app.models.user import User
from datetime import datetime

mock_api_keys = {
    "api_key_1": {
        "id": "user_123",
        "customer_id": "customer_123"
    }
}

mock_dataset_items = [
    ("dataset_1", "item_1"),
]

class MockDatabase:
    def __init__(self, api_keys: dict[str, str] = mock_api_keys, dataset_items: list[tuple[str, str]] = mock_dataset_items) -> None:
        """Mocking a database with tables for API keys and dataset items"""
        self.api_keys = api_keys
        self.dataset_items = set(dataset_items)
    
    def get_user_by_api_key(self, api_key: str) -> Optional[User]:
        """Get a user by API key"""
        if api_key in self.api_keys:
            return User(**self.api_keys[api_key])
        else:
            raise ValueError("API key doesn't exist")
            
    def write_violation(self, violation: dict) -> dict:
        """Write a violation to the database if the dataset item exists"""
        if (violation['dataset_id'], violation['item_id']) in self.dataset_items:
            violation.update({"id": uuid.uuid4()})
            violation.update({"created_at": datetime.now()})
            return violation
        else:
            raise ValueError("Dataset item doesn't exist")

# Initialize mock database
db = MockDatabase()