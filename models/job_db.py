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
    position = Column(String(120), nullable=False)
    description = Column(String(5000), nullable=False)
    link = Column(String(1000), nullable=False)
    date_post = Column(Integer, nullable=False)
