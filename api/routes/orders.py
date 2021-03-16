"""Routes for orders endpoints"""

from api.models.order import Order
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from app import storage


@app_routes.route('/orders', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orders():
    """
    Retrieves the list of all Order objects
    """
    all_orders = storage.all(Order).values()
    list_orders = []
    for order in all_orders:
        list_orders.append(order.to_dict())
    return jsonify(list_orders)


@app_routes.route('/orders/<order_id>', methods=['GET'], strict_slashes=False)
def get_user(order_id):
    """ Retrieves a specific State """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    return jsonify(order.to_dict())


@app_routes.route('/users/<user_id>/orders', methods=['POST'], strict_slashes=False)
def post_order(user_id):
    """
    Creates an Order
    """
    user = storage.get(User, user_id)
    if not user:
        abort(make_response(jsonify({"error": "User not found"}), 404))

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["total", "sub_total", "taxes", "paid"]

    data = request.get_json()

    for needed in needed_attributes:
        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    instance = Order(**data)
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
