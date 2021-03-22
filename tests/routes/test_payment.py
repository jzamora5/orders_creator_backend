# """Testing payment endpoints"""

# import json
# from flask import jsonify
# from flask_jwt_extended import create_access_token, set_access_cookies
# from ..conftest import _get_cookie_from_response
# import pytest
# import time

# order = 6


# @pytest.mark.order(order)
# class TestCreate:

#     def test_non_existing_order(self, test_client, user_data):
#         order_id = "123"

#         response = test_client.post(f'api/order/{order_id}/payments')
#         assert response.status_code == 404
#         assert response.json == {"error": "Order not found"}

#     def test_forbidden_user(self, test_client, user_data):
#         order_id = pytest.second_order_id

#         response = test_client.post(f'api/order/{order_id}/payments')
#         assert response.status_code == 403

#     def test_invalid_json(self, test_client, user_data):
#         order_id = pytest.order_id

#         data = {
#         }

#         response = test_client.post(f'api/order/{order_id}/payments')
#         assert response.status_code == 400
#         assert response.json == {'error': 'Not a JSON'}

#     def test_missing_field(self, test_client, user_data):
#         order_id = pytest.order_id

#         data = {
#             "status": "ok",
#             "payment_type": "card",
#         }

#         response = test_client.post(
#             f'api/order/{order_id}/payments', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 400
#         assert response.json == {'error': 'Missing total'}

#     def test_invalid_total(self, test_client, user_data):

#         order_id = pytest.order_id

#         data = {
#             "status": "ok",
#             "payment_type": "card",
#             "total": "hello"
#         }

#         response = test_client.post(
#             f'api/order/{order_id}/payments', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 400
#         assert response.json == {'error': 'Total must be a valid number'}

#     def test_creation(self, test_client, user_data):
#         order_id = pytest.order_id

#         data = {
#             "status": "ok",
#             "payment_type": "card",
#             "total": 100000
#         }

#         response = test_client.post(
#             f'api/order/{order_id}/payments', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 201

#         response_json = response.json

#         assert response_json["status"] == data["status"]
#         assert response_json["payment_type"] == data["payment_type"]
#         assert response_json["total"] == data["total"]

#         pytest.payment_id = response.json["id"]

#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["second_access_token"])

#         order_id = pytest.second_order_id

#         data = {
#             "status": "processing",
#             "payment_type": "debit",
#             "total": 80000
#         }

#         response = test_client.post(
#             f'api/order/{order_id}/payments', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 201

#         pytest.second_payment_id = response.json["id"]

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         order_id = "123"
#         response = test_client.post(
#             f'api/order/{order_id}/payments')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])


# @pytest.mark.order(order + 1)
# class TestGetAllPayments:
#     """
#     Test for getting orders of user
#     """

#     def test_get_order_not_found(self, test_client, user_data):
#         order_id = "12345"
#         response = test_client.get(f'api/order/{order_id}/payments')
#         assert response.status_code == 404
#         assert response.json == {"error": "Order not found"}

#     def test_forbidden_user(self, test_client, user_data):
#         order_id = pytest.second_order_id

#         response = test_client.get(f'api/order/{order_id}/payments')
#         assert response.status_code == 403
#         assert response.json == {"error": "forbidden"}

#     def test_get_all_payments(self, test_client, user_data):
#         order_id = pytest.order_id

#         response = test_client.get(f'api/order/{order_id}/payments')
#         assert response.status_code == 200
#         assert type(response.json) == list

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         user_id = "123"
#         response = test_client.get(f'api/orders/{user_id}')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])

#         time.sleep(0.1)


# @pytest.mark.order(order + 2)
# class TestGetPayment:
#     """
#     Test for getting an specific payment
#     """

#     def test_get_order_not_found(self, test_client, user_data):
#         order_id = "12345"
#         payment_id = "12345"
#         response = test_client.get(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Order not found"}

#     def test_get_payment_not_found(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = "12345"
#         response = test_client.get(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Payment not found"}

#     def test_get_payment_not_found_different_order(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = pytest.second_payment_id
#         response = test_client.get(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Payment not found"}

#     def test_forbidden_user(self, test_client, user_data):
#         order_id = pytest.second_order_id
#         payment_id = pytest.second_payment_id
#         response = test_client.get(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 403

#     def test_get_payment(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = pytest.payment_id
#         response = test_client.get(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 200

#         data = data = {
#             "status": "ok",
#             "payment_type": "card",
#             "total": 100000
#         }

#         response_json = response.json

#         assert response_json["status"] == data["status"]
#         assert response_json["payment_type"] == data["payment_type"]
#         assert response_json["total"] == data["total"]

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         order_id = pytest.second_order_id
#         payment_id = pytest.second_payment_id
#         response = test_client.get(f'api/order/{order_id}')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])


# @pytest.mark.order(order + 3)
# class TestUpdate:

#     def test_order_not_found(self, test_client, user_data):
#         order_id = "12345"
#         payment_id = "12345"
#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Order not found"}

#     def test_put_payment_not_found(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = "12345"
#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Payment not found"}

#     def test_put_payment_not_found_different_order(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = pytest.second_payment_id
#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Payment not found"}

#     def test_forbidden_user(self, test_client, user_data):
#         order_id = pytest.second_order_id
#         payment_id = pytest.second_payment_id
#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 403

#     def test_update_payment_status(self, test_client, user_data):
#         order_id = pytest.order_id
#         payment_id = pytest.payment_id
#         data = {
#             "status": "rejected",
#         }

#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 200
#         assert response.json["status"] == data["status"]

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         order_id = "12345"
#         payment_id = "12345"
#         response = test_client.put(
#             f'api/order/{order_id}/payments/{payment_id}')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])
