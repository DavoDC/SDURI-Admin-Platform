from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from datetime import date
from app import db #, email
from app.myadmin import bp

# from app.auth.token import * # generate_confirmation_token, confirm_token 
# from app.auth.auth_forms import * # PasswordReset, ChangePasswordForm
from app.forms import LoginForm, RegistrationForm
from app.models import *
from app.controllers import *

# datatables module from flaskk
from datatables import DataTable, DataColumn # ColumnDT, DataTables

@bp.route('/home') #, methods=['GET', 'POST'])
@bp.route('/')
def admin_home():
  # templates/myadmin/index.html
  usersFromDB = User.query.all()
  return render_template('home.html', title="Administrator", users=usersFromDB)
