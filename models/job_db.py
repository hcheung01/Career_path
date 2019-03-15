"""
Skill Job_db from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import backref

class Job_db(BaseModel, Base):
    """Amenity class handles all application amenities"""
    __tablename__ = 'job_db'
    company = Column(String(60), nullable=False)
    location = Column(String(60), nullable=False)
    position = Column(String(60), nullable=False)
    description = Column(String(500), nullable=False)
    level = Column(String(60), nullable=True)
    link = Column(String(500), nullable=False)
    data_post = Column(DateTime, nullable=False)
