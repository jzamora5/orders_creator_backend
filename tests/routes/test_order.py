"""Testing order endpoints"""

import json
from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from ..conftest import _get_cookie_from_response


def test_order(test_client, test_jwt_cookie):
    """
    Test for getting orders
    """

    # Test without cookies
    # response = test_client.get('api/orders')
    # assert response.status_code == 401
    # assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}

    # Test with Cookies

    cookie_name = "access_token_cookie"
    test_client.set_cookie(cookie_name, test_jwt_cookie)

    response = test_client.get('api/orders')
    assert response.status_code == 200
    # assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
