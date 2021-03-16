from flask import Blueprint

app_routes = Blueprint('app_routes', __name__, url_prefix='/api')

from api.routes.users import *  # noqa
from api.routes.orders import *  # noqa
from api.routes.shippings import *  # noqa
from api.routes.payments import *  # noqa
