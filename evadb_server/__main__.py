from flask import Flask
from flask_cors import CORS

from .routes import legacy, next, session


app = Flask(__name__)
CORS(app, supports_credentials=True)

# register single parts of the server
app.register_blueprint(session.app, url_prefix="/")
app.register_blueprint(legacy.app, url_prefix="/legacy")
app.register_blueprint(next.app, url_prefix="/next")


if __name__ == "__main__":
    app.run()
