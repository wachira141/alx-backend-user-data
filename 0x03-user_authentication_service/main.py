#!/usr/bin/env python3
"""
Main file
"""
import requests
from user import User
from auth import Auth

auth = Auth()
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
service_url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """Test creating a new user"""
    route_url = '{}/users'.format(service_url)
    user_payload = {"email": EMAIL, "password": PASSWD}
    response = requests.post(route_url, data=user_payload)
    assert response.status_code == 200
    assert response.json() == {"email": "{}",
                               "message": "user created"
                               .format(email)}
    res = requests.post(route_url, data=user_payload)
    assert response.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password) -> None:
    """Test loggin with a wrong password"""
    route_url = '{}/sessions'.format(service_url)
    user_cred = {"email": email, "password": password}
    response = requests.post(route_url, data=user_cred)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test successfull login"""
    route_url = '{}/sessions'.format(service_url)
    user_cred = {"email": email, "password": password}
    response = requests.post(route_url, data=user_cred)
    assert response.json() == {"email": email, "message": "logged in"}
    assert response.status_code == 200
    response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test if the user is logged"""
    route_url = '{}/profile'.format(service_url)
    res = requests.get(route_url)
    assert res.json() == {"message": "bad request"}
    assert res.status_code == 403


def profile_logged(session_id) -> None:
    """Test if the user profile is loggedin"""
    route_url = '{}/profile'.format(service_url)
    cookie = {
        "session_id": session_id
    }
    res = requests.get(route_url, cookies=cookie)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id) -> None:
    """Test if user can logout"""
    route_url = '{}/sessions'.format(service_url)
    cookie = {
        "session_id": session_id
    }
    res = requests.delete(route_url, cookies=cookie)
    assert res.status_code == 200
    assert res.json == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test requesting for a password reset"""
    url = "{}/reset_password".format(service_url)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a user's password.
    """
    url = "{}/reset_password".format(service_url)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}

# print(User.__tablename__)

# for column in User.__table__.columns:
#     print("{}: {}".format(column, column.type))


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
