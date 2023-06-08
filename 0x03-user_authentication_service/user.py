#!/usr/bin/env python3
"""
module user.py to define class user
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String

Base = declarative_base()


class User(Base):
    """class model to create a user"""
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
