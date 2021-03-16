"""Routes for users endpoints"""

from app import storage
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from api.controllers.auth_controller import AuthController


@app_routes.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


# @app_routes.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
# def get_user(user_id):
#     """ Retrieves a specific State """
#     state = storage.get(User, user_id)
#     if not state:
#         abort(404)

#     return jsonify(state.to_dict())
