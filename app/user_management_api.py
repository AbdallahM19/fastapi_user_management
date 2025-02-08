"""app.py"""

from typing import Annotated, Optional
from re import match
from fastapi import APIRouter, Depends, HTTPException, Form, Query, Response
# from sqlmodel import Session, select, delete, update
from app.database import UserCreate
from app.helper import EMAIL_REGEX, SessionDep, user_helper, res_helper


user_management_apis = APIRouter(
    tags=["user-management-api"],
)


@user_management_apis.get("/login/", operation_id="get_login_page")
async def login():
    """Read login"""
    return {"message": "Login"}

@user_management_apis.post("/login/", operation_id="login_processes")
async def login(
    username: Annotated[str, Form(min_length=3, max_length=100)],
    password: Annotated[str, Form()],
    res: Response,
    session: SessionDep
):
    """Login"""
    try:
        if match(EMAIL_REGEX, username):
            user = user_helper.get_user_by_email(username, session)
        else:
            user = user_helper.get_user_by_username(username, session)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.password != password:
            raise HTTPException(status_code=401, detail="Invalid password")

        res_helper.set_session_id(user.session_id, res)

        return user
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_management_apis.get("/register/", operation_id="get_register_page")
async def read_register():
    """Read register"""
    return {"message": "Register"}

@user_management_apis.post("/register/", operation_id="register_processes")
async def read_register(user: UserCreate, res: Response, session: SessionDep):
    """Register"""
    try:
        user = user_helper.create_user(session, user)
        res_helper.set_session_id(user.session_id, res)
        return user
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_management_apis.delete("/logout/", operation_id="logout_processes")
async def logout(res: Response):
    """Logout"""
    try:
        res_helper.clear_session_id(res)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
