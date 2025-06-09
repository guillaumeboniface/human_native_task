from fastapi import HTTPException, Header
from app.db.mock_db import db
from app.models.user import User

async def verify_api_key(x_api_key: str = Header(...)) -> User:
    """
    Verify the API key from the request header.
    Raises HTTPException if the key is invalid.
    """
    try:
        user = db.get_user_by_api_key(x_api_key)
        return user
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    