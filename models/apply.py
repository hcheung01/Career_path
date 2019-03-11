#!/usr/bin/python3
"""
Apply Class from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, ForeignKey
from sqlalchemy.orm import backref



class Apply(BaseModel, Base):
    """Apply class handles all application status"""
    __tablename__ = 'apply'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('job.id'), nullable=False)
    inteview = Column(String(128), nullable=True)
    status = Column(String(128), nullable=True)
