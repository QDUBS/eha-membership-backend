from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class NotificationBaseSchema(BaseModel):
    user_id: str
    title: str
    description: str
    createdAt: datetime

class NotificationSchema(NotificationBaseSchema):
    class Config():
        from_attributes = True

class ShowNotification(BaseModel):
    user_id: str
    title: str
    description: str
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
