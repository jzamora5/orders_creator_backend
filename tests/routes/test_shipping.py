"""Testing shipping endpoints"""

import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response
import pytest


@pytest.mark.order(3)
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
