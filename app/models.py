from sqlalchemy import Column, String, Boolean, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class EmailLog(Base):
    __tablename__ = "email_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    to_email = Column(String(255), nullable=False, index=True)
    subject = Column(String(500))
    status = Column(String(50))          # queued, sent, failed, bounced
    user_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True))

class SuppressionList(Base):
    __tablename__ = "suppression_list"
    email = Column(String(255), primary_key=True)
    reason = Column(String(100))         # bounce, complaint, unsubscribe
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    permanent = Column(Boolean, default=True)