from app import storage
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from api.utils import encrypt_password
from api.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required


@app_routes.route('/auth/login', methods=['POST'], strict_slashes=False)
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

    user = storage.get_by_attr(User, "email", data["email"]).first()

    if not user:
        abort(make_response(jsonify({"error": "User not found"}), 404))

    # is_valid_password = encrypt_password.is_valid(
    #     user.password.encode(), data["password"])

    is_valid_password = user.password == data["password"]

    if not is_valid_password:
        abort(make_response(jsonify({"error": "Wrong password"}), 404))

    serialized_instance = user.to_dict()

    resp = make_response(jsonify(serialized_instance), 201)

    return AuthController.set_jwt_cookies(resp, user.id)


@app_routes.route('/auth/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout_user():
    """
    Logout a User
    """
    resp = make_response(jsonify(), 201)

    AuthController.remove_jwt_cookies_(resp)

    return resp


@app_routes.route('/auth/register', methods=['POST'], strict_slashes=False)
def register_user():
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

    serialized_instance = instance.to_dict()

    resp = make_response(jsonify(serialized_instance), 201)

    return AuthController.set_jwt_cookies(resp, instance.id)
