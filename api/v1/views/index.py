#!/usr/bin/python3
"""create a Flask api"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """return a JSON"""
    return jsonify({"status": "OK"})
