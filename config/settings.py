from os import getenv

DB_USERNAME = getenv('RDS_USERNAME')
DB_PASSWORD = getenv('RDS_PASSWORD')
DB_HOSTNAME = getenv('RDS_HOSTNAME')
DB_PORT = getenv('RDS_PORT')
DB_NAME = getenv('RDS_DB_NAME')
DB_ENV = getenv('DB_ENV')
