import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response
import pytest
import time
from app import storage
from api.models.user import User

order = 2


@pytest.mark.order(order)
class TestGetAllUsers:
    """Tests for getting all users information"""

    def test_get_users(self, test_client, user_data):
        response = test_client.get(f'api/users/all')
        assert response.status_code == 200

        response_json = response.json
        assert len(response_json) == 2

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        response = test_client.get(f'api/users/all')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])


@pytest.mark.order(order + 1)
class TestGetUser:
    """Tests for getting a user information"""

    def test_get_user_not_found(self, test_client, user_data):
        user_id = "12345"
        response = test_client.get(f'api/users/{user_id}')
        assert response.status_code == 404
        assert response.json == {"error": "User not found"}

    def test_get_user(self, test_client, user_data):

        data = {
            "name": "Marco",
            "last_name": "Polo",
            "email": "marco@email.com",
            "password": "123456789",
            "company": "coderise"
        }

        instance = User(**data)

        instance.save()

        user_id = instance.id

        response = test_client.get(f'api/users/{user_id}')
        assert response.status_code == 200

        response_json = response.json

        assert response_json["name"] == data["name"]
        assert response_json["last_name"] == data["last_name"]
        assert response_json["email"] == data["email"]
        assert response_json.get("password") == None

    def test_no_cookie(self, test_client, user_data):
        test_client.cookie_jar.clear()
        user_id = "12345"
        response = test_client.get(f'api/users/{user_id}')
        assert response.status_code == 401
        assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
        test_client.set_cookie(
            "0.0.0.0", 'access_token_cookie', user_data["access_token"])
