from functools import wraps

from flask import request, jsonify, Response


def jsonrpc(app, route):
    def outer(fn):
        """Define jsonrpc endpoint.

        The function will receive the json data as an parameter.

        The returned object can either be an json-compatible dict or an
        Response object, which will not be further modified.
        """

        @app.route(route, methods=["POST"])
        @wraps(fn)
        def inner(*args, **kwargs):
            data = request.json

            session_cookie = request.cookies.get("session")
            result = fn(data, *args, **kwargs)

            if not isinstance(result, Response):
                result = jsonify(result)

            return result
        return inner
    return outer
