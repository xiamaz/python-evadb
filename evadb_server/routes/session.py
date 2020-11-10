from functools import wraps

from flask import Blueprint, request, jsonify

import evadb

from evadb_server.models.sessionmanager import SessionManager
from .base import jsonrpc
from .. import config

CUSTOM_HOST = config.CUSTOM_HOST or evadb.constants.EVADB_USER_HOST

sessions = SessionManager()
SESSION_COOKIE = "session"


app = Blueprint("login", __name__)


def get_session_id():
    session_id = request.cookies.get(SESSION_COOKIE)
    return session_id


def has_session(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        session_id = get_session_id()
        session = sessions.get(session_id)
        if session is None:
            return {"error": "Failed to get session", "data": None}
        return fn(session, *args, **kwargs)
    return inner


@jsonrpc(app, "/login")
def login(data):
    """Login with data containing {user, password}.

    Will return existing session, if the request contains a session cookie.
    """
    # do not login again, if the client already has a logged session
    session_cookie = request.cookies.get(SESSION_COOKIE)
    session = sessions.get(session_cookie)

    # return existing session if still logged in
    if session and session.check_session():
        return {"error": None, "data": None}

    # delete any existing session
    sessions.delete(session_cookie)

    # generate a new session cookie
    session_cookie = sessions.generate_session_id()

    eva_inst = evadb.EvaDBUser(CUSTOM_HOST).login(user=data["user"], password=data["password"])

    if eva_inst.logged_in:
        sessions.add(session_cookie, eva_inst)
        response = jsonify({"error": None, "data": None})
        # setting secure=True will cause cookie to be not used in
        # python-requests!
        response.set_cookie("session", session_cookie, samesite="None", secure=False)
    else:
        response = {"error": "Failed to login", "data": None,}

    return response


@jsonrpc(app, "/logout")
def logout(_):
    session_id = request.cookies.get(SESSION_COOKIE)
    sessions.delete(session_id)

    return {"error": None, "data": None}
