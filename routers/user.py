from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from sqlalchemy.orm import Session
from schemas.user import UserSchema, ShowUser, CreateUser
from models import user
from db.database import get_db
from utils.hashing import Hash
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post('/', response_model=CreateUser, status_code=status.HTTP_201_CREATED)
def create_user(request: UserSchema, db: Session = Depends(get_db)):

    new_user = user.User(email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user(id: str, response: Response, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    single_user = db.query(user.User).filter(user.User.id == id).first()

    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id of {id} does not exist.")

    return single_user
