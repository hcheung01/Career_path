#!/usr/bin/python3
"""
Place Class from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, DateTime, PickleType, Text
from sqlalchemy.orm import backref

class JobSkill(Base):
    """ PlaceAmenity Class """
    __tablename__ = 'job_skill'
    metadata = Base.metadata
    job_id = Column(String(60),
                      ForeignKey('job.id'),
                      nullable=False,
                      primary_key=True)
    skill_id = Column(String(60),
                        ForeignKey('skills.id'),
                        nullable=False,
                        primary_key=True)


class Job(BaseModel, Base):
    """Place class handles all application places"""
    __tablename__ = 'job'
    company = Column(String(60), nullable=False)
    position = Column(String(120), nullable=False)
    location = Column(String(60), nullable=False)
#    description = Column(String(10000), nullable=True)

    description = Column(Text(), nullable=True)

    applied = Column(String(60), nullable=True)
    interview = Column(String(60), nullable=True)
    status = Column(String(60), nullable=True)
    note = Column(String(300), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    skills = Column(String(500), nullable=True)

#    link = Column(String(5000), nullable=False)
#    date_post = Column(DateTime, nullable=False)
#    html_description = Column(PickleType(), nullable=False)
#    html_description = Column(String(10000), nullable=False)
    html_description = Column(Text(), nullable=False)
