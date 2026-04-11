from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime, timezone
from App.database import Base

"""Defines the URL model for the database"""

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    