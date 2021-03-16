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


@app_routes.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    needed_attributes = ["name", "last_name", "email", "password", "company"]

    for needed in needed_attributes:

        if needed not in request.get_json():
            abort(400, description=f"Missing {needed}")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
