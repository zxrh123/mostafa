"""
Router Model
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Router(Base):
    """Router model"""
    __tablename__ = "routers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    router_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    host = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Should be encrypted in production
    api_port = Column(Integer, default=8728)
    ssh_port = Column(Integer, default=22)
    connection_type = Column(String, default="api")  # api or ssh
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional router info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
