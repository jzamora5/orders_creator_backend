import pytest
from api.models.user import User
from api.models.order import Order

order = 2

TAXES_PERCENTAGE = 19


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


@pytest.mark.order(order)
class TestGetUsersOrders:
    """Tests for getting orders of users list"""

    def test_non_existing_users(self, test_client, user_data):
        user_id_list = ["123", "345"]
        user_ids = ','.join(user_id_list)
        response = test_client.get(f'api/users/{user_ids}')
        assert response.status_code == 200
        response_json = response.json
        assert response_json == []

    def test_existing_users(self, test_client, user_data):

        users = [
            {
                "name": "Marco",
                "last_name": "Polo",
                "email": "marco2@email.com",
                "password": "123456789",
                "company": "coderise"
            },
            {
                "name": "Ramon",
                "last_name": "Perez",
                "email": "ramon2@email.com",
                "password": "123456789",
                "company": "coderise"
            }
        ]

        user_id_list = []
        for user in users:
            instance = User(**user)
            user_id_list.append(instance.id)
            instance.save()

        orders = [
            {
                "sub_total": 600000,
                "status": "procesing"
            },
            {
                "sub_total": 700000,
                "status": "rejected"
            }
        ]

        order_id_list = []
        for i in range(len(orders)):
            instance = Order(**orders[i])
            instance.user_id = user_id_list[i]
            instance.taxes = instance.sub_total * (TAXES_PERCENTAGE / 100)
            instance.total = instance.taxes + instance.sub_total

            order_id_list.append(instance.id)
            instance.save()

        user_ids = ','.join(user_id_list)

        response = test_client.get(f'api/users/{user_ids}')
        assert response.status_code == 200
        response_json = response.json

        assert response_json[0]["sub_total"] == orders[0]["sub_total"]
        assert response_json[0]["status"] == orders[0]["status"]
        assert response_json[1]["sub_total"] == orders[1]["sub_total"]
        assert response_json[1]["status"] == orders[1]["status"]


# @pytest.mark.order(order + 1)
# class TestGetUser:
#     """Tests for getting a user information"""

#     def test_get_user_not_found(self, test_client, user_data):
#         user_id = "12345"
#         response = test_client.get(f'api/users/{user_id}')
#         assert response.status_code == 404
#         assert response.json == {"error": "User not found"}

#     def test_get_user(self, test_client, user_data):

#         data = {
#             "name": "Marco",
#             "last_name": "Polo",
#             "email": "marco@email.com",
#             "password": "123456789",
#             "company": "coderise"
#         }

#         instance = User(**data)

#         instance.save()

#         user_id = instance.id

#         response = test_client.get(f'api/users/{user_id}')
#         assert response.status_code == 200

#         response_json = response.json

#         assert response_json["name"] == data["name"]
#         assert response_json["last_name"] == data["last_name"]
#         assert response_json["email"] == data["email"]
#         assert response_json.get("password") == None

#     def test_no_cookie(self, test_client, user_data):
#         test_client.cookie_jar.clear()
#         user_id = "12345"
#         response = test_client.get(f'api/users/{user_id}')
#         assert response.status_code == 401
#         assert response.json == {'msg': 'Missing cookie "access_token_cookie"'}
#         test_client.set_cookie(
#             "0.0.0.0", 'access_token_cookie', user_data["access_token"])
