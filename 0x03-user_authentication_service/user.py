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
    id: int = Column(INTEGER, primary_key=True, autoincrement=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)
