from api.models.order import Order
from api.models.user import User
from api.models.shipping import Shipping
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import storage


@app_routes.route('/order/<order_id>/shipping', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_shipping(order_id):
    """
    Creates an Shipping
    """

    order = storage.get(Order, order_id)
    if not order:
        abort(make_response(jsonify({"error": "Order not found"}), 404))

    if get_jwt_identity() != order.user_id:
        abort(make_response(jsonify({"error": "forbidden"}), 403))

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["address", "city", "state", "country", "cost"]

    data = request.get_json()

    for needed in needed_attributes:
        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    try:
        float(data["cost"])
    except ValueError:
        abort(make_response(
            jsonify({"error": "Cost must be a valid number"}), 400))

    # instance = Order(**data)
    # instance.user_id = user.id
    # instance.taxes = instance.sub_total * (TAXES_PERCENTAGE / 100)
    # instance.total = instance.taxes + instance.sub_total
    # instance.save()
    # return make_response(jsonify(instance.to_dict()), 201)
