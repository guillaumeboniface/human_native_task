from pydantic import BaseModel

class User(BaseModel):
    id: str
    customer_id: str