#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def get_all_states():
    """
    Retrieve the list of all states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for stste in states]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """show states and states with id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def states_delete(state_id):
    """delete method"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """create a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(404, "Not a JSON")
        data = request.get_json(force=True, silent=True)
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
