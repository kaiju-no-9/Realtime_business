from pydantic import BaseModel

class APIKeyResponse(BaseModel):
    key: str