from fastapi import APIRouter, Depends, HTTPException
from app.models.violation import ViolationRequest
from app.models.user import User
from app.core.security import verify_api_key
from app.db.mock_db import db

router = APIRouter()

@router.post("/violation")
async def create_violation(
        violation: ViolationRequest,
        user: User = Depends(verify_api_key),
    ) -> dict:
    """
    Create a new violation record.
    
    - **dataset_id**: Dataset identifier
    - **item_id**: Violation identifier
    - **jurisdictions**: List of jurisdictions (non-empty), see Jurisdiction enum
    - **type**: Violation type, see ViolationType enum
    """
    violation = violation.model_dump()
    violation['customer_id'] = user.customer_id
    violation['user_id'] = user.id

    # Write the violation to the database
    try:
        violation = db.write_violation(violation)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    return {
        "status": "success",
        "data": violation
    }