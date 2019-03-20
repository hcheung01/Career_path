#!/usr/bin/python3
"""
Skill Class from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import backref

class Skill(BaseModel, Base):
    """Skill class handles all application amenities"""
    __tablename__ = 'skills'
    name = Column(String(128), nullable=False)
