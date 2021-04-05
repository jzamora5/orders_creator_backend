"""Entrypoint for API"""

from api.db.db_storage import DBStorage
from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config/settings.py')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # app.config['CORS_ORIGINS'] = ['localhost', '127.0.0.1']

    JWTManager(app)

    @app.errorhandler(404)
    def not_found(error):
        """ 404 Error
        ---
        responses:
        404:
            description: a resource was not found
        """
        return make_response(jsonify({'error': "Not found"}), 404)

    return app


app = create_app()

with app.app_context():
    storage = DBStorage()
    storage.reload()

    from api.routes import app_routes  # noqa
    app.register_blueprint(app_routes)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()
