from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class SupportTicketBaseSchema(BaseModel):
    user_id: str
    issue: str
    subject: str
    message: str

class SupportTicketSchema(SupportTicketBaseSchema):
    class Config():
        from_attributes = True

class ShowSupportTicket(BaseModel):
    user_id: str
    issue: str
    subject: str
    message: int
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True

