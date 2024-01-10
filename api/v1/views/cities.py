#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, request, jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """show cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [City.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id):
    """delete method"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city(state_id):
    """create a new post req"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if city:
        data = request.get_json(force=True, silent=True)
        if not data:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_id']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """ 404: Not Found """
    return jsonify({'error': "Not Found"}), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Return Bad Request for illegal requess to API
    """
    return jsonify({'error': 'Bad Request'}), 400
