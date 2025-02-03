"""/app/__init__.py"""

from fastapi import FastAPI
from app.database import create_db_and_tables
from app.user_api import user_apis
from app.user_management_api import user_management_apis

app = FastAPI()

app.include_router(user_apis)
app.include_router(user_management_apis)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
