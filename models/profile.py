#!/usr/bin/python3
"""
Place Class from Models Module
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey,\
    MetaData, Table, ForeignKey
from sqlalchemy.orm import backref

class ProfileSkill(Base):
    """ PlaceAmenity Class """
    __tablename__ = 'profile_skill'
    metadata = Base.metadata
    profile_id = Column(String(60),
                      ForeignKey('profile.id'),
                      nullable=False,
                      primary_key=True)
    skill_id = Column(String(60),
                        ForeignKey('skills.id'),
                        nullable=False,
                        primary_key=True)


class Profile(BaseModel, Base):
    """Place class handles all application places"""
    __tablename__ = 'profile'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    position = Column(String(128), nullable=False)
    location = Column(String(1024), nullable=True)
    skills = Column(String(500), nullable=True)
