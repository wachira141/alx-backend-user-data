#!/usr/bin/env python3
"""Hash password and encrypt
"""
import bcrypt
from typing import Union
from uuid import uuid4
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash a bare string password
    @password: a password string to encrypt
    """
    password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return password


class Auth:
    """
    class to auth users credentials
    methods:
        @register_user:
    """
    def __init__(self):
        """init Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> str:
        """public method register_user
            @email: user email str
            @password: user password str
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)

        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """check if password matches
            @email: users email
            @password: users password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                password_match = bcrypt.checkpw(password.encode('utf-8'),
                                                user.hashed_password)
                return password_match
        except NoResultFound:
            return False
        return False

    def _generate_uuid(self) -> str:
        """generate a uuid"""
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """create a user session and save it in the db
            @email: email to find if user exists
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """find a user by session id
            @session_id: the session_id str to identify a user
        """
        if session_id is None:
            return None
        try:
            user_by_session = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user_by_session

    def destroy_session(self, user_id):
        """destroy session
            @user_id: users id to find a user
        """
        if user_id is None:
            return None
        try:
            user_session = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str = None) -> str:
        """generate a password reset token
            @email: a string representing user's email
            Return: return a user password reset token
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None

        if user is None:
            raise ValueError()

        password_res_token = self._generate_uuid()

        self._db.update_user(user.id, reset_token=password_res_token)
        return password_res_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update a user password
            @reset_token: reset_token to find a user
            @password: the new user provided password
            update new user's password and reset_token=None
            Return:
                -None
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_passw = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=new_passw,
                             reset_token=None)
        return None
