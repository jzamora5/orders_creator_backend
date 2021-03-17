from app import app
from flask_jwt_extended import create_access_token
import json
import pytest


def _get_cookie_from_response(response, cookie_name):
    cookie_headers = response.headers.getlist("Set-Cookie")
    for header in cookie_headers:
        attributes = header.split(";")
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split("=")
                cookie[split[0].strip().lower()] = split[1] if len(
                    split) > 1 else True
            return cookie
    return None


@pytest.fixture(scope='module')
def test_client():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="session", autouse=True)
def test_register():
    with app.test_client() as testing_client:
        with app.app_context():
            data = {
                "name": "Larry",
                "last_name": "Hudson",
                "email": "larry@email.com",
                "password": "123456789",
                "company": "personal"
            }

            response = testing_client.post(
                'api/auth/register', data=json.dumps(data), content_type='application/json')


@pytest.fixture(scope='module')
def test_jwt_cookie(test_client):

    data = {
        "email": "larry@email.com",
        "password": "123456789",
    }

    response = test_client.post(
        'api/auth/login', data=json.dumps(data), content_type='application/json')
    access_cookie = _get_cookie_from_response(response, "access_token_cookie")
    access_token = access_cookie["access_token_cookie"]

    return access_token
