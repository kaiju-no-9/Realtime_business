from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import RegisterSchema, LoginSchema
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from api.deps import get_db

router = APIRouter()

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid creds")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}