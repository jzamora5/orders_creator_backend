"""Routes for users endpoints"""

from app import storage
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError


@app_routes.route('/users/all', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_routes.route('/users/<user_id_list>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users_list_orders(user_id_list):
    """ Retrieves a orders for specific users """
    users_ids = user_id_list.split(',')

    orders_list = []
    for user_id in users_ids:
        user = storage.get(User, user_id)
        if not user:
            continue

        for order in user.orders:
            orders_list.append(order.to_dict())

    return jsonify(orders_list)
