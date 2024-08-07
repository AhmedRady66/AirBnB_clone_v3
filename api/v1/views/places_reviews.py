#!/usr/bin/python3
"""Create reviews app"""
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_in_place(place_id):
    """Retrieve all Review objects of a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = storage.all(Review).values()
    place_reviews = [review.to_dict() for review in reviews if review.place_id == place_id]

    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object by review_id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Create a new Review object in a specific Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, "Missing text")

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object by review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    review.save()

    return make_response(jsonify(review.to_dict()), 200)
