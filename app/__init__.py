"""/app/__init__.py"""

from fastapi import FastAPI
from app.database import create_db_and_tables
from app.user_api import user_apis

app = FastAPI()

app.include_router(user_apis, tags=["users-api"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
