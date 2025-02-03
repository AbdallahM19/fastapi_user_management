"""database.py"""

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

class UserBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: Optional[str] = Field(default=None, index=True)

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    email: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


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
    'get_session', 'create_db_and_tables'
]
