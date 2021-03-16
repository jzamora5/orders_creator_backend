"""Entrypoint for API"""

from api.db.db_storage import DBStorage
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)

app.config.from_pyfile('config/settings.py')

with app.app_context():
    storage = DBStorage()
storage.reload()

from api.routes import app_routes  # noqa
app.register_blueprint(app_routes)


# cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)
