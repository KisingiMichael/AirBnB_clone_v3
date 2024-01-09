#!/usr/bin/python3
"""define routes of blueprint
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def get_stats():
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)
    users = storage.count(User)
    return jsonify(stats)
