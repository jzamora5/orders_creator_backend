"""Testing order endpoints without auth"""
import pytest


@pytest.mark.order(1)
def test_create_order(test_client):
    """ Test for creating orders """
    # Clear cookies
    test_client.cookie_jar.clear()

    # Test without cookie
    user_id = "123"
    response = test_client.post('api/users/{user_id}/orders')
    assert response.status_code == 401
    assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}


@pytest.mark.order(2)
def test_get_user_orders(test_client):
    """
    Test for getting user orders
    """

    user_id = "12345"
    response = test_client.get(f'api/orders/{user_id}')
    assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}


@pytest.mark.order(2)
def test_for_updating_order(test_client):
    """
    Test for updating order
    """

    order_id = "123"
    response = test_client.put(f'api/order/{order_id}')
    assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
