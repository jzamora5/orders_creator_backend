"""Routes for orders endpoints"""

from api.models.order import Order
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from app import storage


@app_routes.route('/orders', methods=['GET'], strict_slashes=False)
def get_orders():
    """
    Retrieves the list of all Order objects
    """
    all_orders = storage.all(Order).values()
    list_orders = []
    for order in all_orders:
        list_orders.append(order.to_dict())
    return jsonify(list_orders)


# @app_routes.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
# def get_user(user_id):
#     """ Retrieves a specific State """
#     state = storage.get(User, user_id)
#     if not state:
#         abort(404)

#     return jsonify(state.to_dict())


@app_routes.route('/users/<user_id>/orders', methods=['POST'], strict_slashes=False)
def post_order(user_id):
    """
    Creates an Order
    """
    user = storage.get(User, user_id)
    if not user:
        abort(400, description="User not found")

    if not request.get_json():
        abort(400, description="Not a JSON")

    needed_attributes = ["total", "sub_total", "taxes", "paid"]

    for needed in needed_attributes:
        if needed not in request.get_json():
            abort(400, description=f"Missing {needed}")

    data = request.get_json()
    instance = Order(**data)
    instance.user_id = user.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
