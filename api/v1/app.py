#!/usr/bin/python3
"""Endpoint (route) will be to return the status of your API"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# creating a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def teardown(self):
    """Removes the current SQLAlchemy Session"""
    return storage.close()


if getenv("HBNB_API_HOST"):
    host = getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if getenv("HBNB_API_PORT"):
    port = int(getenv("HBNB_API_PORT"))
else:
    port = 5000


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
