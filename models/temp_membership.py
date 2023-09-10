from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, event, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from db.database import Base
from datetime import datetime
from sqlalchemy.ext.mutable import MutableDict
import uuid


class TempMembership(Base):
    __tablename__ = 'temp_membership'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    category = Column(String, index=True)
    plan = Column(String, index=True)
    noOfBeneficiaries = Column(Integer, index=True)
    noOfDependants = Column(Integer, index=True)
    totalBeneficiariesDependants = Column(Integer, index=True)
    planType = Column(MutableDict.as_mutable(JSONB), index=True)
    recurrence = Column(String, index=True)
    startDate = Column(String, index=True)
    endDate = Column(String, index=True)
    primaryHolderName = Column(String, index=True)
    primaryHolderEmail = Column(String, index=True)
    primaryHolderFirstname = Column(String, index=True)
    primaryHolderLastname = Column(String, index=True)
    primaryHolderMobile = Column(String, index=True)
    primaryHolderBeneficiaryStatus = Column(String, index=True)
    beneficiaries = Column(MutableDict.as_mutable(JSONB), index=True)
    dependants = Column(MutableDict.as_mutable(JSONB), index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", uselist=False, back_populates="temp_membership")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(TempMembership, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
