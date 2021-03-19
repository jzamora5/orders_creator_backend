"""Testing payment endpoints"""

import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response
import pytest
import time

order = 6


@pytest.mark.order(order)
class TestCreate:

    def test_non_existing_order(self, test_client, user_data):
        order_id = "123"

        response = test_client.post(f'api/order/{order_id}/payment')
        assert response.status_code == 404
        assert response.json == {"error": "Order not found"}

    def test_forbidden_user(self, test_client, user_data):
        order_id = pytest.second_order_id

        response = test_client.post(f'api/order/{order_id}/payment')
        assert response.status_code == 403

    def test_invalid_json(self, test_client, user_data):
        order_id = pytest.order_id

        data = {
        }

        response = test_client.post(f'api/order/{order_id}/payment')
        assert response.status_code == 400
        assert response.json == {'error': 'Not a JSON'}

    def test_missing_field(self, test_client, user_data):
        order_id = pytest.order_id

        data = {
            "status": "ok",
            "payment_type": "card",
        }

        response = test_client.post(
            f'api/order/{order_id}/payment', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Missing total'}

    def test_invalid_total(self, test_client, user_data):

        order_id = pytest.order_id

        data = {
            "status": "ok",
            "payment_type": "card",
            "total": "hello"
        }

        response = test_client.post(
            f'api/order/{order_id}/payment', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Total must be a valid number'}

    def test_creation(self, test_client, user_data):
        order_id = pytest.order_id

        data = {
            "status": "ok",
            "payment_type": "card",
            "total": 100000
        }

        response = test_client.post(
            f'api/order/{order_id}/payment', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 201

        response_json = response.json

        assert response_json["status"] == data["status"]
        assert response_json["payment_type"] == data["payment_type"]
        assert response_json["total"] == data["total"]

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        order_id = "123"
        response = test_client.post(
            f'api/order/{order_id}/payment')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])
