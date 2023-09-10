from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from schemas.beneficiary import BeneficiarySchema, ShowBeneficiary
from schemas.user import UserSchema
from datetime import datetime
from models import beneficiary
from db.database import get_db
from utils.oauth2 import get_current_user
import uuid

router = APIRouter(
    prefix="/beneficiaries",
    tags=['Beneficiaries']
)


@router.get('/', response_model=List[ShowBeneficiary], status_code=status.HTTP_200_OK)
def get_beneficiaries(db: Session = Depends(get_db)):
    beneficiaries = db.query(beneficiary.Beneficiary).all()

    return beneficiaries


@router.get('/{id}', response_model=ShowBeneficiary, status_code=status.HTTP_200_OK)
def get_beneficiary(id: str, db: Session = Depends(get_db)):
    single_beneficiary = db.query(beneficiary.Beneficiary).filter(beneficiary.Beneficiary.id == id).first()

    if not single_beneficiary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Beneficiary with id of {id} does not exist.")

    return single_beneficiary


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_beneficiary(request: BeneficiarySchema, db: Session = Depends(get_db)):
    new_beneficiary = beneficiary.Beneficiary(user_id=request.user_id, beneficiary_id=request.beneficiary_id, firstname=request.firstname, lastname=request.lastname,
                                               membership_status=request.membership_status, dob=request.dob, gender=request.gender, age=request.age, beneficiary_no=request.beneficiary_no)
    db.add(new_beneficiary)
    db.commit()
    db.refresh(new_beneficiary)

    return new_beneficiary


@router.post('/create-multiple', status_code=status.HTTP_201_CREATED)
def create_multiple_beneficiaries(*, beneficiaries_batch: List[BeneficiarySchema], db: Session = Depends(get_db)):
    beneficiaries = []
    
    for beneficiary_object in beneficiaries_batch:
        beneficiary_dict = beneficiary_object.model_dump()
        beneficiary_dict['id'] = str(uuid.uuid4().hex)
        beneficiary_dict['createdAt'] = datetime.utcnow()
        beneficiaries.append(beneficiary_dict)

    db.bulk_insert_mappings(beneficiary.Beneficiary, beneficiaries)
    db.commit()
    
    return beneficiaries
