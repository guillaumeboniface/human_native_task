from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Jurisdiction(str, Enum):
    US = "us"
    EU = "eu"

class ViolationType(str, Enum):
    PRIVACY = "privacy"

class ViolationRequest(BaseModel):
    dataset_id: str = Field(
        description="Dataset identifier",
        min_length=1,
    )
    item_id: str = Field(
        description="Data item identifier",
        min_length=1,
    )
    jurisdictions: List[Jurisdiction] = Field(
        min_length=1,
        description="List of jurisdictions",
    )
    type: ViolationType = Field(
        description="Violation type",
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "dataset_id": "dataset_123",
                "item_id": "item_123",
                "jurisdictions": [Jurisdiction.US, Jurisdiction.EU],
                "type": ViolationType.PRIVACY
            }
        }