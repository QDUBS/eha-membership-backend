from typing import List
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class ProfileBaseSchema(BaseModel):
    user_id: str
    name: str
    mobile_number: str
    photo: str
    also_beneficiary: bool

class ProfileSchema(ProfileBaseSchema):
    class Config():
        from_attributes = True

class ShowProfile(BaseModel):
    user_id: str
    name: str
    mobile_number: str
    photo: str
    also_beneficiary: bool
    createdAt: datetime
    updatedAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
