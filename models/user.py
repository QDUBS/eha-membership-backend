from sqlalchemy import Column, String, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
from enum import Enum
import uuid


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    membership = relationship("Membership", uselist=False, back_populates="user", cascade="all, delete-orphan")
    temp_membership = relationship("TempMembership", uselist=False, back_populates="user", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="user", cascade="all, delete-orphan")
    dependants = relationship("Dependant", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    support_tickets = relationship("SupportTicket", back_populates="user", cascade="all, delete-orphan")
    saved_payments = relationship("SavedPayment", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)  # Generate a unique 32-character ID

    @property
    def profile_data(self):
        if self.profile is None:
            return None
        return self.profile
    
    @property
    def membership_data(self):
        if self.membership is None:
            return None
        return self.membership
    
    @property
    def temp_membership_data(self):
        if self.temp_membership is None:
            return None
        return self.temp_membership


@event.listens_for(User, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
