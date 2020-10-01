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

@bp.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
  pass
@bp.route('/display/users/page/<int:page_num>', methods=['GET', 'POST']) # , defaults={'input_ppage': 5})
def display_users(page_num):
  print("page_num: ", page_num)
  input_ppage=3 # default value
  print("request.args: ", request.args)
  print("len(request.args): ", len(request.args))
  # Typecast from string to int
  input_ppage = input_ppage
  if request.method == "GET" and len(request.args) != 0 and request.args != None:
    input_ppage = int(request.args.get('input_ppage'))
    print("request.args.get(input_ppage): ", request.args.get('input_ppage'))
  print("inpu_ppage, page_num: ", input_ppage, page_num)
  usersFromDB = User.query.paginate(per_page=input_ppage, page=page_num, error_out=True)
  # usersFromDB = user_serializer.dump(userFromDB.items)

  return render_template('users.html', title="Administrator", users=usersFromDB)

@bp.route('/delete_selected', methods=['GET', 'POST'])
def delete_selected():
  pass

@bp.route('/add/user', methods=['GET', 'POST'])
def add_user():
  data = request.form
  flash_msg = ""
  form = RegistrationForm()
  if request.method == 'POST':
    print("data: ", data)
    user = User(name=data['name'],
                email=data['email'],
                confirmed=False,
                password='password', # Must send password reset email
                registered_on=date.today(),
                role=data['role'])
    db.session.add(user)
    db.session.commit()
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('/auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email and reset your password"
    email.send_email(user.email, subject, html)
    flash_msg = "Email has been sent to the new user"
  flash(flash_msg)
  return redirect(url_for('myadmin.display_users', page_num=1))

@bp.route('/multiple_emails', methods=['GET', 'POST'])
def multiple_emails():
  pass
  