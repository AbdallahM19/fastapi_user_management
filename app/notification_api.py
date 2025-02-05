"""/app/notification_api.py"""

from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks
from app.helper import EMAIL_REGEX, user_helper, res_helper, notification_helper


notification_apis = APIRouter(
    tags=["notification-api"],
)


@notification_apis.get("/receive-notification/{email}")
async def receive_notification(
    email: Annotated[str, EMAIL_REGEX],
    background_tasks: BackgroundTasks
):
    """Receive notification"""
    background_tasks.add_task(notification_helper.receive_notification_task, email)
    return {"message": "Notification received"}


@notification_apis.post("/send-notification/{email}")
async def send_notification(
    email: Annotated[str, EMAIL_REGEX],
    background_tasks: BackgroundTasks
):
    """Send notification"""
    background_tasks.add_task(notification_helper.send_notification_task, email, message="some notification")
    return {"message": "Notification sent"}
