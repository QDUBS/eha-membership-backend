from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class ShowProfile(BaseModel):
    user_id: str
    name: str
    mobile_number: str
    photo: str
    also_beneficiary: bool
    createdAt: datetime
    updatedAt: datetime


class MembershipBaseSchema(BaseModel):
    user_id: str
    primary_holder_id: str
    membership_id: str
    state: str
    name: str
    start_date: datetime
    end_date: datetime
    total_beneficiaries: int
    total_dependents: int
    total_qty: int
    membership_type: str
    category: str
    plan: str


class MembershipSchema(MembershipBaseSchema):
    class Config():
        from_attributes = True


class ShowMembership(BaseModel):
    user_id: str
    primary_holder_id: str
    membership_id: str
    state: str
    name: str
    start_date: datetime
    end_date: datetime
    total_beneficiaries: int
    total_dependents: int
    total_qty: int
    membership_type: str
    category: str
    plan: str
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
