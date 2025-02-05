"""app.py"""

from typing import Annotated, Optional
from re import match
from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlmodel import Session, select, delete, update
from app.helper import EMAIL_REGEX, user_helper, res_helper


user_management_apis = APIRouter(
    tags=["user-management-api"],
)


@user_management_apis.get("/login/")
async def login():
    """Read login"""
    return {"message": "Login"}

@user_management_apis.post("/login/")
async def login(
    username: Annotated[str, Form(min_length=3, max_length=100)],
    password: Annotated[str, Form()]
):
    """Login"""
    try:
        if match(EMAIL_REGEX, username):
            user = user_helper.get_user_by_email(username)
        else:
            user = user_helper.get_user_by_username(username)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid password")

        return {"username": username, "password": password}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_management_apis.get("/register/")
async def read_register(username: str = Query(...), password: str = Form(...)):
    return {"username": username, "password": password}

@user_management_apis.post("/register/")
async def read_register(username: str = Query(...), password: str = Form(...)):
    return {"username": username, "password": password}

@user_management_apis.delete("/logout/")
async def read_logout(username: str = Query(...)):
    return {"username": username}
