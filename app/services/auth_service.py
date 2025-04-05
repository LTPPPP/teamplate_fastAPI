from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.hash import bcrypt
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.jwt import create_access_token

def register_user(db: Session, user_data: UserCreate):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=bcrypt.hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user_data: UserLogin):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not bcrypt.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
