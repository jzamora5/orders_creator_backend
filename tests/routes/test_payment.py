"""Testing payment endpoints"""

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
