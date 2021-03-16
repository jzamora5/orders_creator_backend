"""Routes for users endpoints"""

from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from app import storage


@app_routes.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_states = storage.all(User).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


# @app_routes.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
# def get_user(user_id):
#     """ Retrieves a specific State """
#     state = storage.get(User, user_id)
#     if not state:
#         abort(404)

#     return jsonify(state.to_dict())
