from __future__ import print_function
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from db.odoo import api
from sqlalchemy.orm import Session
from models import temp_membership
from schemas.user import UserSchema
from schemas.temp_membership import TempMembershipSchema, ShowTempMembership
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/temp_membership",
    tags=["Temp Membership"],
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_temp_membership(request: TempMembershipSchema, db: Session = Depends(get_db)):
    new_temp_membership = temp_membership.TempMembership(user_id=request.user_id, category=request.category, plan=request.plan, noOfBeneficiaries=request.noOfBeneficiaries, 
                                                        noOfDependants=request.noOfDependants, totalBeneficiariesDependants=request.totalBeneficiariesDependants, 
                                                        planType=request.planType, recurrence=request.recurrence, startDate=request.startDate, endDate=request.endDate, 
                                                        primaryHolderName=request.primaryHolderName, primaryHolderEmail=request.primaryHolderEmail, 
                                                        primaryHolderFirstname=request.primaryHolderFirstname, primaryHolderLastname=request.primaryHolderLastname,
                                                        primaryHolderMobile=request.primaryHolderMobile, primaryHolderBeneficiaryStatus=request.primaryHolderBeneficiaryStatus,
                                                        beneficiaries=request.beneficiaries, dependants=request.dependants)
    
    db.add(new_temp_membership)
    db.commit()
    db.refresh(new_temp_membership)

    return new_temp_membership


@router.get('/', response_model=ShowTempMembership, status_code=status.HTTP_200_OK)
def get_temp_membership(user_id: str, db: Session = Depends(get_db)):
    single_temp_membership = db.query(temp_membership.TempMembership).filter(temp_membership.TempMembership.user_id == user_id).first()

    return single_temp_membership


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_temp_membership(id: str, request: TempMembershipSchema, db: Session = Depends(get_db)):
    single_temp_membership = db.query(temp_membership.TempMembership).filter(temp_membership.TempMembership.id == id)
    if not single_temp_membership.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Temp Membership with id of {id} does not exist.")

    single_temp_membership.update({'id': id, 'user_id': request.user_id, 'category': request.category, 'plan': request.plan, 'noOfBeneficiaries': request.noOfBeneficiaries, 
                                   'noOfDependants': request.noOfDependants, 'totalBeneficiariesDependants': request.totalBeneficiariesDependants, 'planType': request.planType, 
                                   'recurrence': request.recurrence, 'startDate': request.startDate, 'endDate': request.endDate, 'primaryHolderName': request.primaryHolderName, 
                                   'primaryHolderEmail': request.primaryHolderEmail, 'primaryHolderFirstname': request.primaryHolderFirstname, 
                                   'primaryHolderLastname': request.primaryHolderLastname, 'primaryHolderMobile': request.primaryHolderMobile, 
                                   'primaryHolderBeneficiaryStatus': request.primaryHolderBeneficiaryStatus, 
                                   'beneficiaries': request.beneficiaries, 'dependants': request.dependants})

    db.commit()

    return single_temp_membership
