#!/usr/bin/env python3
"""DB module
"""
# from uuid import uuid4
from typing import Union
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def reload(self):
        """reload the database"""
        return self._session

    def add_user(self, email: str,
                 hashed_password: str) -> User:
        """add session user to the db
        """
        try:
            user_obj = User(email=email, hashed_password=hashed_password)
            self._session.add(user_obj)
            self._session.commit()
        except Exception:
            self._session.rollback()
            user_obj = None
        return user_obj

    def find_user_by(self, **kwargs) -> User:
        """find a user using the keyword
            @kwargs:
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        user = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if user is None:
            raise NoResultFound()
        return user

        # for user in users:
        #     if user.email == email:
        #         return user
        # raise NoResultFound
    def update_user(self, user_id: int, **kwargs) -> None:
        """update a user
            @user_id: id to identify a single user
            @kwargs: other fields in User's class
        """
        user = self.find_user_by(id=user_id)

        if user is None:
            return None
        update_source = {}
        for key, values in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = values
            else:
                raise ValueError()
        self._session.query(User).filter(
            User.id == user_id
            ).update(update_source, synchronize_session=False,)
        self._session.commit()
