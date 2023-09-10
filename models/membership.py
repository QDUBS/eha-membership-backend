from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class Membership(Base):
    __tablename__ = 'memberships'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    primary_holder_id = Column(String, index=True)
    membership_id = Column(String, index=True)
    state = Column(String, index=True)
    name = Column(String, index=True)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    total_beneficiaries = Column(Integer, index=True)
    total_dependents = Column(Integer, index=True)
    total_qty = Column(Integer, index=True)
    membership_type = Column(String, index=True)
    category = Column(String, index=True)
    plan = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", uselist=False, back_populates="membership")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(Membership, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
