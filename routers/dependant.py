from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from schemas.dependant import DependantSchema, ShowDependant
from schemas.user import UserSchema
from datetime import datetime
from models import dependant
from db.database import get_db
from utils.oauth2 import get_current_user
import uuid

router = APIRouter(
    prefix="/dependants",
    tags=['Dependants']
)


@router.get('/', response_model=List[ShowDependant], status_code=status.HTTP_200_OK)
def get_dependants(db: Session = Depends(get_db)):
    dependants = db.query(dependant.Dependant).all()

    return dependants


@router.get('/{id}', response_model=ShowDependant, status_code=status.HTTP_200_OK)
def get_dependant(id: str, db: Session = Depends(get_db)):
    single_dependant = db.query(dependant.Dependant).filter(dependant.Dependant.id == id).first()

    if not single_dependant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Dependant with id of {id} does not exist.")

    return single_dependant


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_dependant(request: DependantSchema, db: Session = Depends(get_db)):
    new_dependant = dependant.Dependant(user_id=request.user_id, dependant_id=request.dependant_id, firstname=request.firstname, lastname=request.lastname,
                                        membership_status=request.membership_status, dob=request.dob, gender=request.gender, age=request.age,
                                        beneficiary_name=request.beneficiary_name, beneficiary_id=request.beneficiary_id)
    db.add(new_dependant)
    db.commit()
    db.refresh(new_dependant)

    return new_dependant


@router.post('/create-multiple', status_code=status.HTTP_201_CREATED)
def create_multiple_dependants(*, dependants_batch: List[DependantSchema], db: Session = Depends(get_db)):
    dependants = []
    
    for dependant_object in dependants_batch:
        dependant_dict = dependant_object.model_dump()
        dependant_dict['id'] = str(uuid.uuid4().hex)
        dependant_dict['createdAt'] = datetime.utcnow()
        dependants.append(dependant_dict)

    db.bulk_insert_mappings(dependant.Dependant, dependants)
    db.commit()
    
    return dependants
