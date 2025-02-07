"""/app/__init__.py"""

from fastapi import FastAPI
from app.database import create_db_and_tables
from app.user_api import user_apis
from app.user_management_api import user_management_apis
from app.notification_api import notification_apis

app = FastAPI(
    title="FastAPI User Management",
    description="This is a simple user management system built with FastAPI",
    version="0.1.0",
    terms_of_service="https://www.example.com/terms/",
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    openapi_tags=[
        {
            "name": "users-api",
            "description": "User API: Create, read, update, and delete users",
        },
        {
            "name": "user-management-api",
            "description": "User Management API: Login, register, and manage users",
        },
        {
            "name": "notification-api",
            "description": "Notification API: Send and receive notifications",
        },
    ]
)

app.include_router(user_apis)
app.include_router(user_management_apis)
app.include_router(notification_apis)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# {
#   "password": "000",
#   "id": 1,
#   "email": "wolv@email.com",
#   "username": "wolv",
#   "age": 20,
#   "session_id": "3577a29f-fa92-4e88-97cb-9aa04b8b052a"
# }
