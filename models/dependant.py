from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class Dependant(Base):
    __tablename__ = 'dependants'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    dependant_id = Column(Integer, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    membership_status = Column(String, index=True)
    dob = Column(DateTime, index=True)
    gender = Column(String, index=True)
    age = Column(Integer, index=True)
    beneficiary_name = Column(String, index=True)
    beneficiary_id = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="dependants")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(Dependant, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
