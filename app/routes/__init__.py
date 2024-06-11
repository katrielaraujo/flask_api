from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
sales_bp = Blueprint('sales', __name__)

from app.routes.auth import *
from app.routes.sales import *
