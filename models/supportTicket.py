from sqlalchemy import Column, ForeignKey, String, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class SupportTicket(Base):
    __tablename__ = 'support_tickets'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    issue = Column(String, index=True)
    subject = Column(String, index=True)
    message = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="support_tickets")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)  


@event.listens_for(SupportTicket, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
