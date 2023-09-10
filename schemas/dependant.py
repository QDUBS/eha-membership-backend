from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class DependantBaseSchema(BaseModel):
    user_id: str
    dependant_id: int
    firstname: str
    lastname: str
    membership_status: str
    dob: datetime
    gender: str
    age: int
    beneficiary_name: str
    beneficiary_id: str

class DependantSchema(DependantBaseSchema):
    class Config():
        from_attributes = True

class ShowDependant(BaseModel):
    id: str
    user_id: str
    dependant_id: int
    firstname: str
    lastname: str
    membership_status: str
    dob: datetime
    gender: str
    age: int
    beneficiary_name: str
    beneficiary_id: str
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
