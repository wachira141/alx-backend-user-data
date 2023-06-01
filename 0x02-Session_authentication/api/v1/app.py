#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type:
    from api.v1.auth.auth import Auth
    if auth_type == 'auth':
        auth = Auth()
    if auth_type == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    if auth_type == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    if auth_type == 'session_exp_auth':
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    if auth_type == 'session_db_auth':
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()


@app.before_request
def handle_before_req():
    """before request handler
    """
    if auth is not None:
        req_path = request.path
        paths_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
        req_auth = auth.require_auth(req_path, paths_list)

        req_headers = request.headers
        if req_auth:
            auth_header = auth.authorization_header(request)
            auth_session = auth.session_cookie(request)

            if auth_header is None and auth_session is None:
                abort(401)

            current_usr = auth.current_user(request)
            if current_usr is None:
                abort(403)
            request.current_user = current_usr


@app.errorhandler(401)
def un_authorized(error) -> str:
    """Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_route(error) -> str:
    """forbidden route handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
