from fastapi import FastAPI
from app.api import auth
from app.db.session import init_db

app = FastAPI(title="FastAPI Backend", version="1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
