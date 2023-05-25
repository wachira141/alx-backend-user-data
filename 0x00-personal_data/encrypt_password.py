#!/usr/bin/env python3
'''
Module to encrypt a text based password
'''
import bcrypt


def hash_password(password: str) :
    '''function to hash a password
    '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_pw: bytes, password: str) -> bool:
    """check if a hashed passw is formed from the given password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)
