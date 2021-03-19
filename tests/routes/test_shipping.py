"""Testing shipping endpoints"""

import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response
import pytest
import time

order = 9


@pytest.mark.order(order)
class TestCreate:
    def test_non_existing_order(self, test_client, user_data):
        order_id = "123"

        response = test_client.post(f'api/order/{order_id}/shipping')
        assert response.status_code == 404
        assert response.json == {"error": "Order not found"}

    def test_forbidden_user(self, test_client, user_data):
        order_id = pytest.second_order_id

        response = test_client.post(f'api/order/{order_id}/shipping')
        assert response.status_code == 403

    def test_invalid_json(self, test_client, user_data):
        order_id = pytest.order_id

        data = {
        }

        response = test_client.post(f'api/order/{order_id}/shipping')
        assert response.status_code == 400
        assert response.json == {'error': 'Not a JSON'}

    def test_missing_field(self, test_client, user_data):
        order_id = pytest.order_id

        data = {
            "address": "Marylan 12 Street",
            "state": "California",
            "country": "Colombia",
            "cost": 25000
        }

        response = test_client.post(
            f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Missing city'}

    def test_invalid_cost(self, test_client, user_data):

        order_id = pytest.order_id

        data = {
            "address": "Marylan 12 Street",
            "city": "San Francisco",
            "state": "California",
            "country": "Colombia",
            "cost": "hello"
        }

        response = test_client.post(
            f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Cost must be a valid number'}

    def test_creation(self, test_client, user_data):
        order_id = pytest.order_id
        # print("Cheese")
        # print(order_id)
        data = {
            "address": "Marylan 12 Street",
            "city": "San Francisco",
            "state": "California",
            "country": "Colombia",
            "cost": 25000
        }

        response = test_client.post(
            f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 201

        response_json = response.json

        assert response_json["address"] == data["address"]
        assert response_json["city"] == data["city"]
        assert response_json["state"] == data["state"]
        assert response_json["country"] == data["country"]
        assert response_json["cost"] == data["cost"]

    # def test_second_creation(self, test_client, user_data):
    #     order_id = pytest.order_id

    #     data = {
    #         "address": "Marylan 12 Street",
    #         "city": "San Peter",
    #         "state": "California",
    #         "country": "Colombia",
    #         "cost": 25000
    #     }

    #     response = test_client.post(
    #         f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
    #     assert response.status_code == 400
    #     assert response.json == {'error': 'Shipping already exists'}

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        order_id = "123"
        response = test_client.post(
            f'api/order/{order_id}/shipping')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 1)
class TestGet:

    def test_get_shipping_not_found(self, test_client, user_data):
        order_id = "12345"
        response = test_client.get(f'api/order/{order_id}/shipping')
        assert response.status_code == 404
        assert response.json == {"error": "Order not found"}

    def test_forbidden_user(self, test_client, user_data):
        order_id = pytest.second_order_id
        response = test_client.get(f'api/order/{order_id}/shipping')
        assert response.status_code == 403
        assert response.json == {"error": "forbidden"}

    def test_get_shipping(self, test_client, user_data):
        order_id = pytest.order_id
        print(order_id)
        response = test_client.get(f'api/order/{order_id}/shipping')
        assert response.status_code == 200

        data = {
            "address": "Marylan 12 Street",
            "city": "San Francisco",
            "state": "California",
            "country": "Colombia",
            "cost": 25000
        }

        response_json = response.json

        assert response_json["address"] == data["address"]
        assert response_json["city"] == data["city"]
        assert response_json["state"] == data["state"]
        assert response_json["country"] == data["country"]
        assert response_json["cost"] == data["cost"]

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        order_id = order_id = pytest.order_id
        response = test_client.get(f'api/order/{order_id}/shipping')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 2)
class TestUpdate:

    def test_order_not_found(self, test_client, user_data):
        order_id = "123"
        response = test_client.put(f'api/order/{order_id}/shipping')
        assert response.status_code == 404
        assert response.json == {"error": "Order not found"}

    def test_forbidden_user(self, test_client, user_data):
        order_id = pytest.second_order_id

        response = test_client.put(f'api/order/{order_id}/shipping')
        assert response.status_code == 403
        assert response.json == {"error": "forbidden"}

    def test_update_order_paid(self, test_client, user_data):
        order_id = pytest.order_id
        data = {
            "city": "Colorado",
        }
        response = test_client.put(
            f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json["city"] == "Colorado"

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        order_id = "123"
        response = test_client.put(f'api/order/{order_id}/shipping')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])
