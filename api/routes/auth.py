from app import storage
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from api.controllers.auth_controller import AuthController
from api.utils import encrypt_password


@app_routes.route('/auth', methods=['POST'], strict_slashes=False)
def login_user():
    """
    Logs in a User
    """
    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["email", "password"]

    data = request.get_json()

    for needed in needed_attributes:

        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    user = storage.get_by_attr(User, "email", data["email"])

    if not user:
        abort(make_response(jsonify({"error": "User not found"}), 404))

    is_valid_password = encrypt_password.is_valid(
        user.password.encode(), data["password"])

    if not is_valid_password:
        abort(make_response(jsonify({"error": "Wrong password"}), 404))

    return jsonify(user.to_dict())


@app_routes.route('/auth/new', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User
    """
    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["name", "last_name", "email", "password", "company"]

    data = request.get_json()

    for needed in needed_attributes:

        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    instance = User(**data)

    try:
        instance.save()
    except IntegrityError:
        abort(make_response(jsonify({"error": "Email already exists"}), 400))

    token = AuthController.encode_auth_token(instance.id)

    serialized_instance = instance.to_dict()

    serialized_instance["jwt_token"] = token

    return make_response(jsonify(serialized_instance), 201)
