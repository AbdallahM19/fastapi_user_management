"""/app/user_management_api.py.py"""

from typing import Annotated, Optional
from re import match
from fastapi import APIRouter, Depends, HTTPException, Form, Query, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from sqlmodel import Session, select, delete, update
from app.database import UserCreate
from app.helper import EMAIL_REGEX, SessionDep, user_helper, res_helper


user_management_apis = APIRouter(
    tags=["user-management-api"],
)

templates = Jinja2Templates(directory="app/templates")


@user_management_apis.get("/login", operation_id="get_login_page", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login_or_register.html",
        {
            "title": "Login",
            "request": request
        }
    )

@user_management_apis.post("/login", operation_id="login_processes")
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

@user_management_apis.get("/register", operation_id="get_register_page")
async def read_register(request: Request):
    """Read register"""
    return templates.TemplateResponse(
        "login_or_register.html",
        {
            "title": "Register",
            "request": request
        }
    )

@user_management_apis.post("/register", operation_id="register_processes")
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

@user_management_apis.get("/dashboard", operation_id="get_dashboard")
async def read_dashboard(session_id: Annotated[str, Depends(res_helper.get_session_id)], session: SessionDep):
    """Read dashboard"""
    return {
        "title": "Dashboard",
        "current user": user_helper.get_user_by_session_id(session_id, session)
    }

@user_management_apis.delete("/logout", operation_id="logout_processes")
async def logout(res: Response):
    """Logout"""
    try:
        res_helper.clear_session_id(res)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
