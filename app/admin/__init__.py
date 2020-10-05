from flask import Blueprint

bp = Blueprint('myadmin', __name__, template_folder='../templates/admin/')

from app.admin import admin_routes