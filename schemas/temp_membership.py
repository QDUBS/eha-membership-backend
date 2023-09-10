from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class PlanType(BaseModel):
    quantity: int
    price: int
    name: str

    class Config():
        from_attributes = True


class Beneficiary(BaseModel):
    firstName: str
    lastName: str
    email: str
    mobile: str
    dateOfBirth: datetime

    class Config():
        from_attributes = True


class Dependant(BaseModel):
    firstName: str
    lastName: str
    email: str
    mobile: str
    dateOfBirth: datetime

    class Config():
        from_attributes = True


class TempMembershipBaseSchema(BaseModel):
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


class TempMembershipSchema(TempMembershipBaseSchema):
    class Config():
        from_attributes = True


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
    createdAt: datetime
    # user: ShowUser

    class Config():
        from_attributes = True
