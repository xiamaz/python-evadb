from functools import wraps
from flask import Blueprint, jsonify, request


from evadb_server.models.sessionmanager import SessionManager
from ..base import jsonrpc


app = Blueprint("next", __name__)
sessions = SessionManager()

SESSION_COOKIE = "session"


def require_login(fn):
    def inner(*args, **kwargs):
        session_cookie = request.cookies.get(SESSION_COOKIE)
        session = sessions.get(session_cookie)
        if session is None:
            return {"error": "Failed to get session", "data": None}
        return fn(session, *args, **kwargs)
    return inner


@jsonrpc(app, "/")
def status(_):
    """Check if online."""
    return {"status": "ok"}


@jsonrpc(app, "/sample/by-id")
@require_login
def sampleById(session, query):
    """Get a single sample by id
    """
    sample_id = query["id"]
    return {"error": None, "data": "Sample"}
