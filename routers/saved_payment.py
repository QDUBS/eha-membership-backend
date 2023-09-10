from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from schemas.saved_payment import SavedPaymentSchema, ShowSavedPayment
from schemas.user import UserSchema
from models import saved_payment
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/saved-payments",
    tags=['Saved Payments']
)


@router.get('/', response_model=List[ShowSavedPayment], status_code=status.HTTP_200_OK)
def get_saved_payments(user_id: str, db: Session = Depends(get_db)):
    saved_payments = db.query(saved_payment.SavedPayment).filter(saved_payment.SavedPayment.user_id == user_id).all()

    return saved_payments


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_saved_payment(request: SavedPaymentSchema, db: Session = Depends(get_db)):
    new_saved_payment = saved_payment.SavedPayment(
        user_id=request.user_id, card_holder=request.card_holder, card_number=request.card_number, expiration=request.expiration, cvc=request.cvc)
    db.add(new_saved_payment)
    db.commit()
    db.refresh(new_saved_payment)

    return new_saved_payment

