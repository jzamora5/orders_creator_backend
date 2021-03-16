from os import getenv

JWT_SECRET_KEY = getenv('SECRET_KEY', "this_is_a_secret")
JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_CSRF_PROTECT = True
JWT_CSRF_CHECK_FORM = True

DB_USERNAME = getenv('RDS_USERNAME')
DB_PASSWORD = getenv('RDS_PASSWORD')
DB_HOSTNAME = getenv('RDS_HOSTNAME')
DB_PORT = getenv('RDS_PORT')
DB_NAME = getenv('RDS_DB_NAME')
DB_ENV = getenv('DB_ENV')
