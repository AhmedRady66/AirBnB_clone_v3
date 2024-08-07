#!/usr/bin/python3
"""Create places app"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_in_city(city_id):
    """Retrieve all Place objects in a specific City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places if place.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object in a specific City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)
