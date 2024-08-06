#!/usr/bin/python3
"""create a Flask api"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


if __name__ == "__main__":
    H = getenv('HBNB_API_HOST', '0.0.0.0')
    P = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=H, port=P, threaded=True)
