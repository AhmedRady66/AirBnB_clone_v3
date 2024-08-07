#!/usr/bin/python3
"""Create states app"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Return all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """Return state with id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete state with id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    kwargs = request.get_json()
    state = State(**kwargs)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update state with id"""
    if not request.get_json():
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
