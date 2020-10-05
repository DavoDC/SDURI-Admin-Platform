from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

import datetime
from app import db, email
from app.admin import bp

from app.auth.token import * # generate_confirmation_token, confirm_token 
from app.auth.auth_forms import * # PasswordReset, ChangePasswordForm
from app.forms import LoginForm, RegistrationForm
from app.models import *

# @bp.route('/') # ,methods=['GET', 'POST'])
# def myadmin():
#   # templates/myadmin/index.html

#   return render_template('/admin/index.html')