#!/usr/bin/python3
"""Create Flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


if __name__ == "__main__":
    h = getenv('HBNB_API_HOST', '0.0.0.0')
    p = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=h, port=p, threaded=True)
