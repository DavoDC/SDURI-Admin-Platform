from flask import Blueprint

bp = Blueprint('api', __name__, template_folder='../templates/api/')

from app.api import routes