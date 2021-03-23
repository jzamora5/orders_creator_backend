"""Routes for orders endpoints"""

from datetime import datetime
from api.models.order import Order
from api.models.user import User
from api.routes import app_routes
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import storage
from api.utils.sort import sort_response


TAXES_PERCENTAGE = 19


@app_routes.route('/order/<order_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_order(order_id):
    """ Retrieves specific Order """
    order = storage.get(Order, order_id)
    if not order:
        abort(make_response(jsonify({"error": "Order not found"}), 404))

    # if get_jwt_identity() != order.user_id:
    #     abort(make_response(jsonify({"error": "forbidden"}), 403))

    return jsonify()


@app_routes.route('/orders/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_orders(user_id):
    """ Retrieves user Orders """
    user = storage.get(User, user_id)
    if not user:
        abort(make_response(jsonify({"error": "User not found"}), 404))

    # if get_jwt_identity() != user_id:
    #     abort(make_response(jsonify({"error": "forbidden"}), 403))

    orders = storage.get_by_attr(Order, "user_id", user_id)

    orders_list = []
    for order in orders:
        orders_list.append(order.to_dict())

    try:
        sort_response(request, orders_list)
    except KeyError:
        pass

    return jsonify(orders_list)


@app_routes.route('/users/<user_id>/orders', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_order(user_id):
    """
    Creates an Order
    """

    user = storage.get(User, user_id)
    if not user:
        abort(make_response(jsonify({"error": "User not found"}), 404))

    # if get_jwt_identity() != user_id:
    #     abort(make_response(jsonify({"error": "forbidden"}), 403))

    if not request.get_json():
        abort(make_response(jsonify({"error": "Not a JSON"}), 400))

    needed_attributes = ["sub_total", "status"]

    data = request.get_json()

    for needed in needed_attributes:
        if needed not in data:
            abort(make_response(jsonify({"error": f"Missing {needed}"}), 400))

    try:
        float(data["sub_total"])
    except ValueError:
        abort(make_response(
            jsonify({"error": "Subtotal must be a valid number"}), 400))

    instance = Order(**data)
    instance.user_id = user.id
    instance.taxes = instance.sub_total * (TAXES_PERCENTAGE / 100)
    instance.total = instance.taxes + instance.sub_total
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_routes.route('/orders/<order_id_list>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_order_list(order_id_list):
    """ Retrieves a orders for specific users """
    orders_ids = order_id_list.split(',')

    # if len(orders_ids) == 1:
    #     user = storage.get(User, orders_ids[0])
    #     if not user:
    #         abort(make_response(jsonify({"error": "User not found"}), 404))

    orders_list = []
    for order_id in orders_ids:
        order = storage.get(Order, order_id)
        if not order:
            continue

        orders_list.append(order.to_dict())

    try:
        sort_response(request, orders_list)
    except KeyError:
        pass

    return jsonify(orders_list)


@app_routes.route('/orders/shipping', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orders_by_shipment():
    filters = ["address", "city", "state", "country", "cost"]
    args = request.args

    all_orders = storage.all(Order).values()

    list_orders = []
    for order in all_orders:
        check = 1
        for key, value in args.items():
            if key not in filters:
                continue
            value = value.strip().lower()
            current = getattr(order.shipping, key, "").strip().lower()

            if value != current:
                check = 0
                break

        if check:
            order_dict = order.to_dict()
            list_orders.append(order_dict)

    try:
        sort_response(request, list_orders)
    except KeyError:
        pass

    return jsonify(list_orders)


@app_routes.route('/orders/search/<term>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orders_by_term(term):

    all_orders = storage.all(Order).values()
    list_orders = []
    for order in all_orders:
        check = 0
        order_dict = order.to_dict()

        for _, value in order_dict.items():
            if term in str(value).strip().lower():
                check = 1
                break

        if not check and order.shipping:
            shipping_dict = order.shipping.to_dict()
            for _, value in shipping_dict.items():
                if term in str(value).strip().lower():
                    check = 1
                    break

        if not check and order.payments:
            for payment in order.payments:
                payment_dict = payment.to_dict()
                for key, value in payment_dict.items():
                    if term in str(value).strip().lower():
                        check = 1
                        break
                if check:
                    break

        if check:
            order_dict = order.to_dict()
            list_orders.append(order_dict)

    try:
        sort_response(request, list_orders)
    except KeyError:
        pass

    return jsonify(list_orders)


@app_routes.route('/orders/dates/<date_filter>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_orders_by_date(date_filter):

    repetitions, splt_char = 3, '-'
    temp = date_filter.split(splt_char)
    dates = splt_char.join(
        temp[:repetitions]), splt_char.join(temp[repetitions:])

    try:
        start = datetime.strptime(dates[0], '%d-%m-%y')
        end = datetime.strptime(dates[1], '%d-%m-%y')
    except ValueError:
        abort(make_response(
            jsonify({"error": "Dates must comply dd-mm-yy format"}), 404))

    if start > end:
        abort(make_response(
            jsonify({"error": "Dates must comply with start-end"}), 404))

    all_orders = storage.all(Order).values()
    list_orders = []
    for order in all_orders:
        updated_at = order.updated_at
        if start <= updated_at <= end:
            order_dict = order.to_dict()
            list_orders.append(order_dict)

    try:
        sort_response(request, list_orders)
    except KeyError:
        pass

    return jsonify(list_orders)


@app_routes.route('/order/<order_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_order(order_id):
    order = storage.get(Order, order_id)
    if not order:
        abort(make_response(jsonify({"error": "Order not found"}), 404))

    # if get_jwt_identity() != order.user_id:
    #     abort(make_response(jsonify({"error": "forbidden"}), 403))

    ignore = ['id', 'created_at', 'updated_at', "taxes", "total"]
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(order, key, value)

    storage.save()

    return make_response(jsonify(order.to_dict()), 200)
