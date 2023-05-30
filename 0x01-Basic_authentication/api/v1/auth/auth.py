#!/usr/bin/env python3
"""
module to contain a class that will
manage the API authentication
"""
import re
from flask import request
from typing import List, TypeVar


class Auth():
    """
    class Auth to manage auth for the API
    """

    def __init__(self):
        """initialize Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method
            return None - request is a Flask req object
        """
        if request is None:
            return None
        rj = request.get('Authorization', None)
        if rj is None:
            return None

        return rj

    def current_user(self, request=None) -> TypeVar('User'):
        """public method
            return None - request is a Flask req object
        """
        return None
