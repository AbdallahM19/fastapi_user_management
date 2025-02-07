"""database.py"""

from typing import Annotated, Optional

from fastapi import Form
from sqlmodel import Field, Session, SQLModel, create_engine

EMAIL_REGEX = r"^([a-z]+)((([a-z]+)|(_[a-z]+))?(([0-9]+)|(_[0-9]+))?)*@([a-z]+).([a-z]+)$"


class UserBase(SQLModel):
    age: int | None = Field(default=None, index=True)
    username: str = Field(min_length=3, max_length=24, unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, unique=True, primary_key=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    password: Optional[str] = Field(default=None, index=True)
    session_id: Optional[str] = Field(default=None, unique=True, index=True)

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    email: Annotated[str, Form(max_length=100, pattern=EMAIL_REGEX)]
    password: str = Form(...)

class UserUpdate(UserBase):
    username: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


class NotificationBase(SQLModel):
    datetime: Optional[str] = Field(default=None, index=True)
    message: str = Field(index=True)
    email: str = Field(index=True)

class Notification(NotificationBase, table=True):
    id: Optional[int] = Field(default=None, unique=True, primary_key=True)
    user_id: Optional[int] = Field(default=None, index=True)
    is_read: bool = Field(default=False, index=True)


sqlite_file_name = "database.db"

engine = create_engine(
    url=f"sqlite:///{sqlite_file_name}",
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


__all__ = [
    'User', 'UserBase', 'UserPublic', 'UserCreate', 'UserUpdate',
    'Notification', 'NotificationBase',
    'get_session', 'create_db_and_tables',
    'EMAIL_REGEX',
]
