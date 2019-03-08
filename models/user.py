#!/usr/bin/python3
"""
User Class from Models Module
"""
import hashlib
from flask_login import UserMixin
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float


class User(BaseModel, Base, UserMixin):
    """
        User class handles all application users
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone = Column(String(20), nullable=True)

    # apply = relationship('Apply', backref='user', cascade='delete')
    # profile = relationship('Profile', backref='user', cascade='delete')

    def __init__(self, *args, **kwargs):
        """
            instantiates user object
        """
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__set_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __set_password(self, pwd):
        """
            custom setter: encrypts password to MD5
        """
        secure = hashlib.md5()
        secure.update(pwd.encode("utf-8"))
        secure_password = secure.hexdigest()
        setattr(self, "password", secure_password)

    def is_authenticated(self):
        return True
