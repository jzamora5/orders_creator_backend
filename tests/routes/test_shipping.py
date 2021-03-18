"""Testing shipping endpoints"""

import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response
import pytest

order = 6


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
            "cost": 25000
        }

        response = test_client.post(
            f'api/order/{order_id}/shipping', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.json == {'error': 'Cost must be a valid number'}
