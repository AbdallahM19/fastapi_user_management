"""/app/helper.py"""

from re import match
from uuid import uuid4
from typing import Annotated, Optional
from fastapi import Depends, Response, Cookie, HTTPException
from sqlmodel import Session, select, delete, update
from app.database import *

SessionDep = Annotated[Session, Depends(get_session)]


class UserHelper():
    def __init__(self):
        """Initialize UserHelper"""
        pass

    def get_user_by_username(self, username: str, session: SessionDep):
        """Get user by username"""
        return session.exec(select(User).where(User.username == username)).first()

    def get_user_by_email(self, email: str, session: SessionDep):
        """Get user by email"""
        return session.exec(select(User).where(User.email == email)).first()

    def get_user_by_id(self, user_id: int, session: SessionDep):
        """Get user by id"""
        return session.get(User, user_id)

    def get_user_by_session_id(self, session_id: str, session: SessionDep):
        """Get user by session id"""
        return session.exec(select(User).where(User.session_id == session_id)).first()

    def get_all_users(self, session: SessionDep, offset: int = 0, limit: int = 100):
        """Get all users"""
        return session.exec(select(User).offset(offset).limit(limit)).all()

    def create_user(self, session: SessionDep, user: UserCreate):
        """Create user"""
        if self.get_user_by_username(user.username, session):
            raise HTTPException(status_code=400, detail="Username already exists")

        if self.get_user_by_email(user.email, session):
            raise HTTPException(status_code=400, detail="Email already exists")

        db_user = User.model_validate(user)
        db_user.session_id = self.generate_session_id()

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    def update_user_by_id(self, user_id: int, user: UserUpdate, session: SessionDep):
        """Update user"""
        user_db = self.get_user_by_id(user_id, session)
        if not user_db:
            return None
        user_data = user.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(user_data)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db

    def generate_session_id(self) -> str:
        """Generate session id"""
        return str(uuid4())

    def check_email_match(self, email: str):
        """Check email match"""
        return match(EMAIL_REGEX, email)


class ResponseHelper():
    def __init__(self):
        """Initialize ResponseHelper"""
        pass

    @staticmethod
    def get_session_id(session_id: str = Cookie(None)) -> Optional[str]:
        """Get session id from cookie"""
        if not session_id:
            return None
        return session_id

    @staticmethod
    def set_session_id(session_id: str, res: Response):
        """Set session id to response"""
        res.set_cookie("session_id", session_id)

    @staticmethod
    def clear_session_id(res: Response):
        """Clear session id from response"""
        res.delete_cookie("session_id")


class NotificationHelper():
    def __init__(self):
        """Initialize NotificationHelper"""
        pass

    def get_notifications(self, user_id: int, session: SessionDep):
        """Get notifications"""
        return session.exec(
            select(Notification).where(Notification.user_id == user_id)
        ).all()

    def mark_notification_as_read(self, notification_id: int, session: SessionDep):
        """Mark notification as read"""
        notification = session.exec(
            select(Notification).where(Notification.id == notification_id)
        ).first()

        if not notification:
            return None

        notification.is_read = True
        session.add(notification)
        session.commit()
        return notification

    def send_notification_task(self, email: str, message: str, session: SessionDep):
        """Send notification task"""
        user = user_helper.get_user_by_email(email, session)
        if not user:
            return None

        new_notification = Notification(user_id=user.id, email=email, message=message)
        session.add(new_notification)
        session.commit()

    # def receive_notification_task(self, email: str):
    #     """Receive notification task"""
    #     with open("log.txt", mode="r") as email_file:
    #         content = email_file.read()
    #         print(content)


user_helper = UserHelper()
res_helper = ResponseHelper()
notification_helper = NotificationHelper()
