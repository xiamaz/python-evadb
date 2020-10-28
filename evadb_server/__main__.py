from functools import wraps

import uuid
from flask import Flask, jsonify, request
import evadb


app = Flask(__name__)
sessions = {}


def generate_session_id():
    return str(uuid.uuid4())


def get_session():
    session_id = request.cookies.get("session")
    session = sessions.get(session_id)
    return session


def require_login(fn):
    """Require login otherwise return an error response."""

    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        session = get_session()
        if session is None or not session.logged_in:
            return jsonify({"error": "Not logged in"})
        return fn(*args, **kwargs)

    return wrapped_fn


@app.route("/")
def status():
    """Quickly check the health of the server. To be extended."""
    return jsonify({"logged_in": len(sessions)})


@app.route("/login", methods=["POST"])
def login():
    # do not login again, if the client already has a logged session
    session_id = request.cookies.get("session")
    if session_id in sessions:
        return jsonify({"error": None, "data": {"logged_in": sessions[session_id].logged_in}})

    data = request.json

    session_id = generate_session_id()
    eva_inst = evadb.EvaDBUser().login(user=data["user"], password=data["password"])

    sessions[session_id] = eva_inst

    resp = jsonify({"error": None, "data": {"logged_in": eva_inst.logged_in}})
    resp.set_cookie("session", session_id)
    return resp


@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.cookies.get("session")

    if session_id in sessions:
        del sessions[session_id]

    return jsonify({"error": None, "data": None})


@app.route("/search", methods=["GET"])
@require_login
def search():
    """Search autosomal dominant variants."""
    session = get_session()
    if session is None:
        return jsonify({"error": "No session found", "data": None})

    data = request.json
    result = session.search(data)
    return jsonify({"error": None, "data": result})


if __name__ == "__main__":
    app.run()
