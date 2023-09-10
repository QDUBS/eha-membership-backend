from typing import List, Optional, Union, Dict
from pydantic import BaseModel
from datetime import datetime


class ShowProfile(BaseModel):
    user_id: Optional[str]
    name: Optional[str]
    mobile_number: Optional[str]
    photo: Optional[str]
    also_beneficiary: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]

class ShowMembership(BaseModel):
    user_id: Optional[str]
    primary_holder_id: Optional[str]
    membership_id: Optional[str]
    state: Optional[str]
    name: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    total_beneficiaries: Optional[int]
    total_dependents: Optional[int]
    total_qty: Optional[int]
    membership_type: Optional[str]
    category: Optional[str]
    plan: Optional[str]
    createdAt: Optional[datetime]

class ShowTempMembership(BaseModel):
    user_id: str
    category: str
    plan: str
    noOfBeneficiaries: int
    noOfDependants: int
    totalBeneficiariesDependants: int
    planType: Dict
    recurrence: str
    startDate: str
    endDate: str
    primaryHolderName: str
    primaryHolderEmail: str
    primaryHolderFirstname: str
    primaryHolderLastname: str
    primaryHolderMobile: str
    primaryHolderBeneficiaryStatus: str
    beneficiaries: Dict
    dependants: Dict

class BeneficiarySchema(BaseModel):
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

class DependantSchema(BaseModel):
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

class NotificationSchema(BaseModel):
    title: str
    description: str
    createdAt: datetime

class SupportTicketSchema(BaseModel):
    issue: str
    subject: str
    message: str

    class Config():
        from_attributes = True

class UserSchema(BaseModel):
    email: str
    password: str

class CreateUser(BaseModel):
    id: str
    email: str

    class Config():
        from_attributes = True

class ShowUser(BaseModel):
    id: str
    email: str
    profile_data: Union[ShowProfile, None]
    membership_data: Optional[ShowMembership]
    temp_membership_data: Optional[ShowTempMembership]
    beneficiaries: List[BeneficiarySchema] = []
    dependants: List[DependantSchema] = []
    notifications: List[NotificationSchema] = []
    support_tickets: List[SupportTicketSchema] = []

    class Config():
        from_attributes = True
