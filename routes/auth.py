from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database.database import get_session
from models.user import User
from services.auth_service import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post('/register')
def register(req: RegisterRequest, db: Session = Depends(get_session)):
    existing = db.query(User).filter(User.email==req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='User exists')
    user = User(email=req.email, name=req.name, hashed_password=get_password_hash(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, expires_delta=timedelta(hours=12))
    return {"access_token": token}

@router.post('/login')
def login(req: LoginRequest, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email==req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token(user.id, expires_delta=timedelta(hours=12))
    return {"access_token": token}
