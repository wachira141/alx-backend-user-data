#!/usr/bin/env python3
"""app module
    flask app entry point
"""
import os
from flask import Flask, jsonify, request, abort, url_for, redirect
from auth import Auth

app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """app index route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register a user route
        method: POST
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = Auth.register_user(email, password)
        message = {"email": "{}", "message": "user created".format(email)}
        return jsonify(message)
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """login route view
        @formvalues: email and password
        return:
            account login payload
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_login = Auth.valid_login(email, password)

    if valid_login is False:
        abort(401)

    session_id = Auth.create_session(email)
    message = {"email": email, "message": "logged in"}
    response = jsonify(message)
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """respond to a user logout session
        remove the session from the user db
        method=DELETE
        get session id sent as a cookie in the request.cookie obj
    """
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        return jsonify({"message": "bad request"}), 403
    user = Auth.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    Auth.destroy_session(user.id)
    # redirect(url_for("index"))
    redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """get user profile
        methods=GET
        get session_id from the request.cookies obj
    Return:
        - The users infor if found
    """
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        return jsonify({"message": "bad request"}), 400
    user = Auth.get_user_from_session_id(cookie)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """request for a password reset
        methods=POST
        get user's email from form data field.
    """
    email = request.form.get("email", None)
    passw_gen_token = None

    if email is None:
        return jsonify({"message": "bad request"}), 400
    try:
        passw_gen_token = Auth.get_reset_password_token(email)
    except ValueError:
        passw_gen_token = None
    if passw_gen_token is None:
        abort(403)
    payload = {"email": email, "reset_token": passw_gen_token}
    return jsonify(payload), 200


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """update a user password
        Request.form :
                    - email
                    - password
    """
    email = request.form.get("email", None)
    reset_token = request.form.get("reset_token", None)
    new_password = request.form.get("new_password", None)
    if email is None or reset_token is None:
        return jsonify({"message": "bad request"}), 403

    password_changed = False
    try:
        Auth.update_password(reset_token, new_password)
        # check instances when no error but password not changes
        password_changed = True
    except ValueError:
        password_changed = False
    if password_changed is False:
        abort(403)

    payload = {"email": email, "message": "Password updated"}
    return jsonify(payload), 200


if __name__ == "__main__":
    port = os.getenv("APP_PORT")
    host = os.getenv("APP_HOST")
    app.run(host, port, debug=True)
