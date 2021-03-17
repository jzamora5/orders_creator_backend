"""General Endpoints"""
from api.routes import app_routes
from flask import jsonify


@app_routes.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "ok"})
