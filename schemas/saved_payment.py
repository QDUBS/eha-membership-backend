from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class SavedPaymentBaseSchema(BaseModel):
    user_id: str
    card_holder: str
    card_number: str
    expiration: str
    cvc: int

class SavedPaymentSchema(SavedPaymentBaseSchema):
    class Config():
        from_attributes = True

class ShowSavedPayment(BaseModel):
    user_id: str
    card_holder: str
    card_number: str
    expiration: str
    cvc: int
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
