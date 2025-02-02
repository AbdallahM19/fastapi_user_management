"""/app/__init__.py"""

from fastapi import Depends, FastAPI, HTTPException, Query
from app.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
