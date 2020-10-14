from app import db
from app import email
from app.admin import bp
from app.auth.auth_forms import *
from app.auth.token import *
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import *
import datetime
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

# @bp.route('/') # ,methods=['GET', 'POST'])
# def myadmin():
#   # templates/myadmin/index.html

#   return render_template('/admin/index.html')