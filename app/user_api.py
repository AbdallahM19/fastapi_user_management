"""app.py"""

from typing import Annotated, Union, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import delete
from app.database import *
from app.helper import SessionDep, user_helper, res_helper


user_apis = APIRouter(
    prefix="/users",
    tags=["users-api"]
)


@user_apis.get("/", response_model=list[UserBase])
def get_users(users: Annotated[list[User], Depends(user_helper.get_all_users)]):
    return users


@user_apis.get("/me", response_model=Optional[User])
def get_current_user(session_id: Annotated[str, Depends(res_helper.get_session_id)], session: SessionDep):
    return user_helper.get_user_by_session_id(session_id, session)


@user_apis.get("/{user_identifier}", response_model=Union[User, None])
def get_user_by_user_id(user_identifier: Union[int, str], session: SessionDep):
    if isinstance(user_identifier, int) or (isinstance(user_identifier, str) and user_identifier.isdigit()):
        user = user_helper.get_user_by_id(int(user_identifier), session)
    else:
        user = user_helper.get_user_by_username(user_identifier, session)
    return user


@user_apis.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    user: Annotated[User, Depends(user_helper.create_user)],
    res: Response
):
    res_helper.set_session_id(user.session_id, res)
    return user


@user_apis.patch("/{user_id}", response_model=UserPublic)
def update_user(user_db: Annotated[User, Depends(user_helper.update_user_by_id)]):
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db


@user_apis.delete("/{user_id}")
def delete_user(
    user_id: int, session: SessionDep, res: Response
):
    session_id = res_helper.get_session_id(res)
    user = session.get(User, user_id)
    if user and session_id == user.session_id:
        session.delete(user)
        session.commit()
        res_helper.clear_session_id(res)
        return {"ok": True}
    elif session_id != user.session_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    raise HTTPException(status_code=404, detail="User not found")


@user_apis.delete("/")
def delete_all_user(session: SessionDep, res: Response):
    users = session.exec(delete(User))
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    session.commit()
    res_helper.clear_session_id(res)
    return {"ok": True}
