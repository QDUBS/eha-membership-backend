from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    beneficiary_id = Column(Integer, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    membership_status = Column(String, index=True)
    dob = Column(DateTime, index=True)
    gender = Column(String, index=True)
    age = Column(Integer, index=True)
    beneficiary_no = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="beneficiaries")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(Beneficiary, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()


    # id: 952,
    #   firstname: 'Adham',
    #   lastname: 'Hallal',
    #   membership_status: 'confirmed',
    #   dob: '1996-12-20',
    #   gender: 'Male',
    #   age: 26,
    #   beneficiary_no: 'MEM/2023/0003/97'
