import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/fastapi_db")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
