#!/usr/bin/python3
"""Create states app"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """return all states"""
    states = storage.all(State).values
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """return state with id"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', method=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete state with id"""
    state = storage.get(State, state_id)

    if state:
        storage.delete()
        storage.save()
        return make_response(jsonify(), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>', method=['POST'], strict_slashes=False)
def post_state():
    """create state with id"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    state = request.get_json()
    instance = State(**state)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', method=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update state with id"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
