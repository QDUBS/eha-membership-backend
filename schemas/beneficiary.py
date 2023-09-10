from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class BeneficiaryBaseSchema(BaseModel):
    user_id: str
    beneficiary_id: int
    firstname: str
    lastname: str
    membership_status: str
    dob: datetime
    gender: str
    age: int
    beneficiary_no: str

class BeneficiarySchema(BeneficiaryBaseSchema):
    class Config():
        from_attributes = True

class ShowBeneficiary(BaseModel):
    id: str
    user_id: str
    beneficiary_id: int
    firstname: str
    lastname: str
    membership_status: str
    dob: datetime
    gender: str
    age: int
    beneficiary_no: str
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
