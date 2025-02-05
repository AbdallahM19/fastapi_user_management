"""app.py"""

from typing import Annotated, Optional
from re import match
from fastapi import APIRouter, Depends, HTTPException, Form, Query, Response
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
    password: Annotated[str, Form()],
    res: Response
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

        res_helper.set_session_id(user["session_id"], res)

        return {"username": username, "password": password}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_management_apis.get("/register/")
async def read_register():
    """Read register"""
    return {"message": "Register"}

@user_management_apis.post("/register/")
async def read_register(
    username: Annotated[str, Form(min_length=3, max_length=24)],
    email: Annotated[str, Form(max_length=100, regex=EMAIL_REGEX)],
    res: Response,
    password: str = Form(...)
):
    """Register"""
    try:
        user = user_helper.get_user_by_username(username)
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")

        user = user_helper.get_user_by_email(email)
        if user:
            raise HTTPException(status_code=400, detail="Email already exists")

        user = user_helper.create_user(username, email, password)
        res_helper.set_session_id(user["session_id"], res)
        return user
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_management_apis.delete("/logout/")
async def read_logout(username: str = Query(...)):
    return {"username": username}
