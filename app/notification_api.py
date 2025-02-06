"""/app/notification_api.py"""

from typing import Annotated, Union, Optional

from fastapi import APIRouter, BackgroundTasks, Response
from fastapi.routing import APIRoute
from app.helper import SessionDep, user_helper, res_helper, notification_helper
from app.database import NotificationBase, Notification


async def get_notifications(
    session: SessionDep,
    res: Response,
    email: Optional[str] = None,
):
    """Get notifications"""
    if user_helper.check_email_match(email):
        user = user_helper.get_user_by_email(email, session)
    else:
        user = user_helper.get_user_by_session_id(
            res_helper.get_session_id(res), session
        )

    if user:
        return notification_helper.get_notifications(user.id, session)

    return None


async def mark_notification_as_read(
    notification_id: int,
    session: SessionDep,
    background_tasks: BackgroundTasks
):
    """Mark a notification as read"""
    background_tasks.add_task(notification_helper.mark_notification_as_read, notification_id, session)
    return {"message": "Notification marked as read"}


async def send_notification(
    email: str,
    message: str,
    session: SessionDep,
    background_tasks: BackgroundTasks,
):
    """Send notification"""
    if not user_helper.check_email_match(email):
        return {"message": "Invalid email"}

    background_tasks.add_task(notification_helper.send_notification_task, email, message, session)
    return {"message": "Notification sent"}


routes = [
    APIRoute(
        "/get-notifications/{email}", endpoint=get_notifications,
        response_model=Union[list[Notification], Notification, None],
        methods=["GET"], tags=["notification-api"]
    ),
    APIRoute(
        "/mark-as-read/{notification_id}", endpoint=mark_notification_as_read,
        methods=["PUT"], tags=["notification-api"]
    ),
    APIRoute(
        "/send-notification/{email}", endpoint=send_notification,
        methods=["POST"], tags=["notification-api"]
    ),
]


notification_apis = APIRouter(routes=routes)


# @notification_apis.get("/receive-notification/{email}")
# async def receive_notification(
#     background_tasks: BackgroundTasks,
#     email: Optional[str] = None,
# ):
#     """Receive notification"""
#     if not user_helper.check_email_match(email):
#         return {"message": "Invalid email"}

#     background_tasks.add_task(notification_helper.receive_notification_task, email)
#     return {"message": "Notification received"}
