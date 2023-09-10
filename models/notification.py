from sqlalchemy import Column, ForeignKey, String, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    title = Column(String, index=True)
    description = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="notifications")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(Notification, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
