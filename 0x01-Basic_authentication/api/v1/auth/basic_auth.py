#!/usr/bin/env python3
"""Basic auth
    inherit form class Auth
"""

import re
import base64
import binascii
from typing import Tuple, TypeVar

from auth import Auth
from models.user import User

class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth class
    """
    
    def extract_base64_authorization_header(self, authorization_header) -> str:
        """return a Base64 auth header"""
        if authorization_header is None \
            or type(authorization_header) is not str:
            return None
        pattern = r'Basic (<?P<token>.+)'
        auth_header = re.fullmatch(pattern, authorization_header.strip())
        if auth_header is not None:
            return auth_header.group('token')

        return None
    
    def decode_base64_authorization_header(self, 
        base64_authorization_header: str) -> str:
        """decode a Base64 string"""
        if base64_authorization_header is None \
            or type(base64_authorization_header) is not str:
            return None
        
        try:
            base64_str = base64_authorization_header.encode('utf-8')
            base64_str = base64.b64decode(base64_str, validate=True)
            message = base64_str.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None
        return message
    
    def extract_user_credentials(self, \
        decoded_base64_authorization_header: str) -> Tuple[str]:
        """extract user credentials from the base64 decoded value"""
        if decoded_base64_authorization_header is None \
            or type(decoded_base64_authorization_header) is not str:
            return (None, None)
        
        pattern = r'(?P<user>[^:]+):(?P<password>.+)'
        match_str = re.fullmatch(pattern, decoded_base64_authorization_header.strip())
        
        if match_str is None:
            return None, None

        user = match_str.group('user')
        password = match_str.group('password')
        return user, password
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
         """return an instance of a user based on the email passed"""
         if type(user_email) == str and type(user_pwd) == str:
                try:
                    users = User.search({'email': user_email})
                except Exception:
                    return None
                if len(users) <= 0:
                    return None
                if users[0].is_valid_password(user_pwd):
                    return users[0]
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)