from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from models.api_key import APIKey
from models.user import User
from schemas.api_key import APIKeyResponse

router = APIRouter()

# Create API Key (after login)
@router.post("/", response_model=APIKeyResponse)
def create_api_key(user_email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    api_key = APIKey(user_id=user.id)

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {"key": api_key.key}

@router.get("/")
def get_api_keys(user_email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    keys = db.query(APIKey).filter(APIKey.user_id == user.id).all()

    return keys