import os

project_name = "./"
folders = [
    "app",
    "app/api",
    "app/core",
    "app/models",
    "app/schemas",
    "app/services",
    "app/db",
]

files = {
    "main.py": """
from fastapi import FastAPI
from app.api import auth
from app.db.session import init_db

app = FastAPI(title="FastAPI Backend", version="1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
""",
    "app/api/auth.py": """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import register_user, login_user
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)
""",
    "app/models/user.py": """
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
""",
    "app/schemas/user.py": """
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
""",
    "app/services/auth_service.py": """
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
""",
    "app/core/config.py": """
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/fastapi_db")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
""",
    "app/core/jwt.py": """
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import JWT_SECRET

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
""",
    "app/db/base.py": """
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
""",
    "app/db/session.py": """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL
from app.db.base import Base
from app.models import user

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    "Dockerfile": """
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yml": """
version: '3.8'

services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/fastapi_db
      - JWT_SECRET=your_jwt_secret
    depends_on:
      - db

volumes:
  postgres_data:
""",
    "requirements.txt": """
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose
passlib[bcrypt]
pydantic
""",
    ".env": """
DATABASE_URL=postgresql://postgres:password@db:5432/fastapi_db
JWT_SECRET=your_jwt_secret
"""
}


def create_structure():
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    for filepath, content in files.items():
        with open(filepath.replace("/", os.sep), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    print(f"[✅] Project '{project_name}' created successfully!")


if __name__ == "__main__":
    create_structure()
