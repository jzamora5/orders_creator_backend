"""Testing order endpoints"""

import json
from api.models.user import User
from api.models.order import Order
from api.models.shipping import Shipping
import pytest


order = 4
TAXES_PERCENTAGE = 17


@pytest.mark.order(order)
class TestCreate:
    """Tests for Creating Orders"""

    def test_non_existing_user(self, test_client, user_data):
        user_id = "12345"

        response = test_client.post(f'api/users/{user_id}/orders')
        assert response.status_code == 404
        assert response.json == {"error": "User not found"}

    # def test_forbidden_user(self, test_client, user_data):
    #     user_id = user_data["second_user_id"]

    #     response = test_client.post(f'api/users/{user_id}/orders')
    #     assert response.status_code == 403
    #     assert response.json == {"error": "forbidden"}

    def test_invalid_json(self, test_client, user_data):
        user_id = user_data["user_id"]

        data = {
        }

        response = test_client.post(
            f'api/users/{user_id}/orders', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Not a JSON'}

    def test_missing_field(self, test_client, user_data):
        user_id = user_data["user_id"]

        data = {
            "paid": False,
            "status": 'in_progress'
        }

        response = test_client.post(
            f'api/users/{user_id}/orders', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Missing sub_total'}

    def test_invalid_sub_total(self, test_client, user_data):

        user_id = user_data["user_id"]

        data = {
            "sub_total": "Hello",
            "status": 'in_progress'
        }

        response = test_client.post(
            f'api/users/{user_id}/orders', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Subtotal must be a valid number'}

    def test_valid_creation(self, test_client, user_data):

        user_id = user_data["user_id"]

        data = {
            "sub_total": 500000,
            "status": 'in_progress'
        }

        response = test_client.post(
            f'api/users/{user_id}/orders', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 201

        pytest.order_id = response.json["id"]

        response_json = response.json

        assert response_json["sub_total"] == data["sub_total"]
        assert response_json["status"] == data["status"]
        assert response_json["paid"] == False
        assert response_json["taxes"] == data["sub_total"] * (19/100)
        assert response_json["total"] == data["sub_total"] * \
            (19/100) + data["sub_total"]

        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["second_access_token"])

        user_id = user_data["second_user_id"]

        data = {
            "sub_total": 300000,
            "status": 'in_progress'
        }

        response = test_client.post(
            f'api/users/{user_id}/orders', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 201

        pytest.second_order_id = response.json["id"]

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        user_id = "123"
        response = test_client.post(f'api/users/{user_id}/orders')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 1)
class TestGetAllUserOrders:
    """
    Test for getting orders of user
    """

    def test_get_order_not_found(self, test_client, user_data):
        user_id = "12345"
        response = test_client.get(f'api/orders/users/{user_id}')
        assert response.status_code == 404
        assert response.json == {"error": "User not found"}

    def test_get_all_orders(self, test_client, user_data):
        user_id = user_data["user_id"]

        response = test_client.get(f'api/orders/users/{user_id}')
        assert response.status_code == 200
        assert type(response.json) == list

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        user_id = "123"
        response = test_client.get(f'api/orders/{user_id}')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 2)
class TestGetOrder:
    """
    Test for getting an specific order
    """

    def test_get_order_not_found(self, test_client, user_data):
        order_id = "12345"
        response = test_client.get(f'api/order/{order_id}')
        assert response.status_code == 404
        assert response.json == {"error": "Order not found"}

    # def test_forbidden_user(self, test_client, user_data):
    #     order_id = pytest.second_order_id

    #     response = test_client.get(f'api/order/{order_id}')
    #     assert response.status_code == 403

    # def test_get_order(self, test_client, user_data):
    #     order_id = pytest.order_id
    #     # time.sleep(0.2)
    #     response = test_client.get(f'api/order/{order_id}')
    #     assert response.status_code == 200

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        order_id = "123"
        response = test_client.get(f'api/order/{order_id}')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 3)
class TestGetOrdersList:
    """Tests for getting orders of order list"""

    def test_non_existing_orders(self, test_client, user_data):
        order_id_list = ["123", "345"]
        orders_ids = ','.join(order_id_list)
        response = test_client.get(f'api/orders/{orders_ids}')
        assert response.status_code == 200
        response_json = response.json
        assert response_json == []

    def test_existing_order(self, test_client, user_data):
        users = [
            {
                "name": "Marco",
                "last_name": "Polo",
                "email": "marco@email.com",
                "password": "123456789",
                "company": "coderise"
            },
            {
                "name": "Ramon",
                "last_name": "Perez",
                "email": "ramon@email.com",
                "password": "123456789",
                "company": "coderise"
            }
        ]

        user_id_list = []
        for user in users:
            instance = User(**user)
            user_id_list.append(instance.id)
            instance.save()

        orders = [
            {
                "sub_total": 600000,
                "status": "procesing"
            },
            {
                "sub_total": 700000,
                "status": "rejected"
            }
        ]

        order_id_list = []
        for i in range(len(orders)):
            instance = Order(**orders[i])
            instance.user_id = user_id_list[i]
            instance.taxes = instance.sub_total * (TAXES_PERCENTAGE / 100)
            instance.total = instance.taxes + instance.sub_total

            order_id_list.append(instance.id)
            instance.save()

        order_ids = ','.join(order_id_list)
        response = test_client.get(f'api/orders/{order_ids}')
        assert response.status_code == 200
        response_json = response.json

        assert response_json[0]["sub_total"] == orders[0]["sub_total"]
        assert response_json[0]["status"] == orders[0]["status"]
        assert response_json[1]["sub_total"] == orders[1]["sub_total"]
        assert response_json[1]["status"] == orders[1]["status"]


@pytest.mark.order(order + 4)
class TestGetOrdersList:
    """Tests for getting orders based on shipping filter"""

    def test_non_existing_orders(self, test_client, user_data):
        response = test_client.get(f'api/orders/shipping?city=Oklahoma')
        assert response.status_code == 200
        response_json = response.json
        assert response_json == []

    def test_existing_order(self, test_client, user_data):
        users = [
            {
                "name": "Marco",
                "last_name": "Polo",
                "email": "marcopolo@email.com",
                "password": "123456789",
                "company": "coderise"
            }
        ]

        user_id_list = []
        for user in users:
            instance = User(**user)
            user_id_list.append(instance.id)
            instance.save()

        orders = [
            {
                "sub_total": 600000,
                "status": "procesing"
            },
            {
                "sub_total": 700000,
                "status": "rejected"
            },
            {
                "sub_total": 80000,
                "status": "ok"
            },
            {
                "sub_total": 50000,
                "status": "canceled"
            },
        ]

        shippings = [
            {
                "address": "Street Bona Vibra",
                "city": "Denver",
                "state": "Colorado",
                "country": "USA",
                "cost": 450000
            },
            {
                "address": "Sillicon Street",
                "city": "San Francisco",
                "state": "California",
                "country": "USA",
                "cost": 500000
            },
            {
                "address": "Street Bona Food",
                "city": "Denver",
                "state": "Colorado",
                "country": "USA",
                "cost": 680000
            },
            {
                "address": "Street Empire Jay",
                "city": "New York",
                "state": "New York",
                "country": "USA",
                "cost": 325000
            },
        ]

        order_id_list = []
        for i in range(len(orders)):
            instance = Order(**orders[i])
            instance.user_id = user_id_list[0]
            instance.taxes = instance.sub_total * (TAXES_PERCENTAGE / 100)
            instance.total = instance.taxes + instance.sub_total

            order_id_list.append(instance.id)
            instance.save()

            instance = Shipping(**shippings[i])
            instance.order_id = order_id_list[i]
            instance.save()

        response = test_client.get(
            f'api/orders/shipping?city=Denver&state=Colorado')
        assert response.status_code == 200
        response_json = response.json

        assert response_json[0]["status"] == orders[0]["status"]
        assert response_json[1]["status"] == orders[2]["status"]


# @pytest.mark.order(order + 3)
# class TestUpdateOrder:
#     """
#     Test for updating order
#     """

#     def test_order_not_found(self, test_client, user_data):
#         order_id = "123"
#         response = test_client.put(f'api/order/{order_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "Order not found"}

#     def test_forbidden_user(self, test_client, user_data):
#         order_id = pytest.second_order_id

#         response = test_client.put(f'api/order/{order_id}')
#         assert response.status_code == 403
#         assert response.json == {"error": "forbidden"}

#     def test_update_order_paid(self, test_client, user_data):
#         order_id = pytest.order_id
#         data = {
#             "paid": True,
#         }
#         response = test_client.put(
#             f'api/order/{order_id}', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 200
#         assert response.json["paid"] == True

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         order_id = "123"
#         response = test_client.put(f'api/order/{order_id}')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])
