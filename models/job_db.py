"""
Skill Job_db from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime, PickleType, Text
from sqlalchemy.orm import backref



class Job_db(BaseModel, Base):
    """Amenity class handles all application amenities"""
    __tablename__ = 'job_db'
    company = Column(String(60), nullable=False)
    location = Column(String(60), nullable=False)
    position = Column(String(120), nullable=False)
#    description = Column(String(10000), nullable=False)
    description = Column(Text(), nullable=False)
    link = Column(String(5000), nullable=False)
    date_post = Column(Integer, nullable=False)

#    html_description = Column(PickleType(), nullable=False)
    html_description = Column(Text(), nullable=False)
