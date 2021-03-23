"""Routes for users endpoints"""

from app import storage
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from api.utils.sort import sort_response


@app_routes.route('/users/all', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        user_dict = user.to_dict()
        # del user_dict["order"]
        list_users.append(user_dict)

    try:
        sort_response(request, list_users)
    except KeyError:
        pass

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
            order_dict = order.to_dict()
            orders_list.append(order_dict)

    return jsonify(orders_list)
