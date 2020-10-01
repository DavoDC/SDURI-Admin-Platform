from flask import Blueprint

bp = Blueprint('myadmin', __name__, template_folder="../templates/myadmin/")

from app.myadmin import myadmin_routes
