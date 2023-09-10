from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class SavedPayment(Base):
    __tablename__ = 'saved_payments'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    card_holder = Column(String, index=True)
    card_number = Column(String, index=True)
    expiration = Column(String, index=True)
    cvc = Column(Integer, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="saved_payments")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(SavedPayment, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
