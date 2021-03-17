""" Controller for Authentication """

from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                set_access_cookies,
                                set_refresh_cookies,
                                unset_jwt_cookies
                                )


class AuthController:

    @staticmethod
    def set_jwt_cookies(response, identity):
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    @staticmethod
    def remove_jwt_cookies_(response):
        unset_jwt_cookies(response)

        return response
