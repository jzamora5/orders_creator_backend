from api.models.order import Order
from api.models.user import User
from api.models.payment import Payment
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import storage
from time import sleep


@app_routes.route('/order/<order_id>/payments', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_payment(order_id):
    """
    Creates a Payment
    """

    order = storage.get(Order, order_id)
    if not order:
        abort(make_response(jsonify({"error": "Order not found"}), 404))

    if get_jwt_identity() != order.user_id:
        abort(make_response(jsonify({"error": "forbidden"}), 403))

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["status", "payment_type", "total"]

    data = request.get_json()

    for needed in needed_attributes:
        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    try:
        float(data["total"])
    except ValueError:
        abort(make_response(
            jsonify({"error": "Total must be a valid number"}), 400))

    instance = Payment(**data)
    instance.order_id = order_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)
