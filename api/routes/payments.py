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


@app_routes.route('/order/<order_id>/payments', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_payments(order_id):
    order = storage.get(Order, order_id)
    if not order:
        abort(make_response(jsonify({"error": "Order not found"}), 404))

    if get_jwt_identity() != order.user_id:
        abort(make_response(jsonify({"error": "forbidden"}), 403))

    payments = order.payments

    payments_list = []
    for payment in payments:
        payments_list.append(payment.to_dict())

    return jsonify(payments_list)


# @app_routes.route('/order/<order_id>/payments/<payment_id>', methods=['GET'], strict_slashes=False)
# @jwt_required()
# def get_payment(order_id, payment_id):
#     order = storage.get(Order, order_id)
#     if not order:
#         abort(make_response(jsonify({"error": "Order not found"}), 404))

#     payment = storage.get(Payment, payment_id)
#     if not payment:
#         abort(make_response(jsonify({"error": "Payment not found"}), 404))

#     if payment.order.id != order.id:
#         abort(make_response(jsonify({"error": "Payment not found"}), 404))

#     if get_jwt_identity() != order.user_id:
#         abort(make_response(jsonify({"error": "forbidden"}), 403))

#     payment_dict = payment.to_dict()
#     del payment_dict["order"]

#     return jsonify(payment_dict)


# @app_routes.route('/order/<order_id>/payments/<payment_id>', methods=['PUT'], strict_slashes=False)
# @jwt_required()
# def put_payment(order_id, payment_id):
#     order = storage.get(Order, order_id)
#     if not order:
#         abort(make_response(jsonify({"error": "Order not found"}), 404))

#     payment = storage.get(Payment, payment_id)
#     if not payment:
#         abort(make_response(jsonify({"error": "Payment not found"}), 404))

#     if payment.order.id != order.id:
#         abort(make_response(jsonify({"error": "Payment not found"}), 404))

#     if get_jwt_identity() != order.user_id:
#         abort(make_response(jsonify({"error": "forbidden"}), 403))

#     ignore = ['id', 'created_at', 'updated_at']
#     data = request.get_json()
#     for key, value in data.items():
#         if key not in ignore:
#             setattr(payment, key, value)

#     payment.save()

#     payment_dict = payment.to_dict()
#     del payment_dict["order"]

#     return make_response(jsonify(payment_dict), 200)
