from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from datetime import date
from app import db, email
from app.myadmin import bp

from app.auth.token import * # generate_confirmation_token, confirm_token 
from app.auth.auth_forms import * # PasswordReset, ChangePasswordForm
from app.forms import LoginForm, RegistrationForm
from app.models import *

@bp.route('/home') #, methods=['GET', 'POST'])
@bp.route('/')
def admin_home():
  # templates/myadmin/index.html
  usersFromDB = User.query.all()
  return render_template('home.html', title="Administrator", users=usersFromDB)

@bp.route('/update', methods = ['GET', 'POST'])
def update():
  # request.form = ImmutableMultiDict([('id', '2'), ('name', 'supervisor111'), ('email', 'super1@supers.com')])
  # type(request.form) = <class 'werkzeug.datastructures.ImmutableMultiDict'>
  # The tuples' values can be accessed in this format: request.form['id']
  data = request.form 
  flash_msg = ""
  if request.method == 'POST':
    
    # new_data = User.query.filter_by(id=update_id)
    new_data = User.query.get(request.form['id'])
    print("new_data: ", new_data)
    new_data.name = request.form['name']
    new_data.email = request.form['email']
    new_data.role = request.form['role']
    
    db.session.commit()
    flash_msg = new_data.name + "'s information is updated successfully"
  flash(flash_msg)
  # return render_template('home.html', user)
  return redirect(url_for('myadmin.display_users',  page_num=1))

@bp.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
  del_user = User.query.get(id)
  db.session.delete(del_user)
  db.session.commit()
  flash("User Deleted Successfully")

  return redirect(url_for('myadmin.display_users', page_num=1))

@bp.route('/display/users/all/<int:page_num>', methods=['GET', 'POST'])
def display_users(page_num):
  usersFromDB = User.query.paginate(per_page=2, page=page_num, error_out=True)
  # usersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('users.html', title="Administrator", users=usersFromDB)

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
