from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.login import Token
from models import user
from db.database import get_db
from utils.hashing import Hash
from utils.token import create_access_token

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=Token)
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    single_user = db.query(user.User).filter(
        user.User.email == request.username).first()

    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials.")

    if not Hash.verify(single_user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Password is not correct.")

    access_token = create_access_token(data={"sub": single_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": single_user}
