#!/usr/bin/python3
"""
Place Class from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, DateTime
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
    position = Column(String(60), nullable=False)
    level = Column(String(60), nullable=False)
    location = Column(String(60), nullable=False)
    description = Column(String(1000), nullable=True)
    applied = Column(String(60), nullable=True)
    interview = Column(String(60), nullable=True)
    status = Column(String(60), nullable=True)
    note = Column(String(300), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    skills = relationship('Skill', secondary="job_skill",
                             viewonly=False)
