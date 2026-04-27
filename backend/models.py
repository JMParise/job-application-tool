from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from backend.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_url = Column(Text, nullable=False, unique=True)

    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)

    match_score = Column(Integer, default=0)
    status = Column(String, default="Not Applied")

    created_at = Column(DateTime, default=datetime.utcnow)