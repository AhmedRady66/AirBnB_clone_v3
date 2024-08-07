#!/usr/bin/python3
"""Create Flask app"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """description: a resource was not found"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    h = getenv('HBNB_API_HOST', '0.0.0.0')
    p = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=h, port=p, threaded=True)
