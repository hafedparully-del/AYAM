from flask import Blueprint

bp = Blueprint('customer', __name__, template_folder='../../templates/customer')

from . import routes