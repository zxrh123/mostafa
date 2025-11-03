"""
Execution Log Model
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class ExecutionLog(Base):
    """Execution log model"""
    __tablename__ = "execution_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String, unique=True, nullable=False, index=True)
    router_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=True, index=True)
    script = Column(Text, nullable=False)
    status = Column(String, nullable=False)  # success, error, dry_run, etc.
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    dry_run = Column(Boolean, default=True)
    requires_confirmation = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
