"""Testing index endpoints"""


def test_status(test_client):
    """
    Test for status
    """

    # Create a test client using the Flask application configured for testing

    response = test_client.get('api/status')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}
