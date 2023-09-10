from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from schemas.notification import NotificationSchema, ShowNotification
from schemas.user import UserSchema
from models import notification
from db.database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/notifications",
    tags=['Notifications']
)


@router.get('/', response_model=List[ShowNotification], status_code=status.HTTP_200_OK)
def get_notifications(user_id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    notifications = db.query(notification.Notification).filter(notification.Notification.user_id == user_id).all()

    return notifications


@router.get('/{id}', response_model=ShowNotification, status_code=status.HTTP_200_OK)
def get_notification(id: str, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    single_notification = db.query(notification.Notification).filter(
        notification.Notification.id == id).first()

    if not single_notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Notification with id of {id} does not exist.")

    return single_notification


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_notification(request: NotificationSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    new_notification = notification.Notification(
        user_id=request.user_id, title=request.title, description=request.description)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification
