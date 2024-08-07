#!/usr/bin/python3
"""Create Flask app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ close storage """
    storage.close()


@app.error_handler(404)
def not_found(error):
    """not found error message"""
    return jsonify({"error": "NOT FOUND"}), 404


if __name__ == "__main__":
    h = getenv('HBNB_API_HOST', '0.0.0.0')
    p = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, host=h, port=p, threaded=True)
