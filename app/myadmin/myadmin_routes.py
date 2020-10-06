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
from app.myadmin.myadmin_models import *
import datetime

@bp.route('/home') #, methods=['GET', 'POST'])
@bp.route('/')
def admin_home():
  # templates/myadmin/index.html
  usersFromDB = User.query.all()
  tasks_unresolved = AdminTask.query.filter_by(resolved=False)
  tasks_resolved = AdminTask.query.filter_by(resolved=True)
  return render_template('home.html', title="Administrator",
                          users=usersFromDB, unresolved_tasks=tasks_unresolved,
                          resolved_tasks=tasks_resolved)

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
    flash_msg = new_data.email + "'s information is updated successfully"
  flash(flash_msg)
  # return render_template('home.html', user)
  return redirect(url_for('myadmin.display_users',  page_num=1))

@bp.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
  del_user = User.query.get(id)
  db.session.delete(del_user)
  db.session.commit()
  flash("Successfully deleted a user '" + del_user.email + "'")

  return redirect(url_for('myadmin.display_users', page_num=1))

@bp.route('/display/users/all/<int:page_num>', methods=['GET', 'POST'])
def display_users(page_num):
  usersFromDB = User.query.paginate(per_page=2, page=page_num, error_out=True)
  # usersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('users.html', title="Administrator", users=usersFromDB)

@bp.route('/display/students/all/<int:page_num>', methods=['GET', 'POST'])
def display_students(page_num):
  col_names = Student.__table__.columns
  colNames = [i.name.capitalize() for i in col_names] # Capitalize columns' name
  attributes = [i.name for i in col_names] # Columns' name
  studentsFromDB = Student.query.paginate(per_page=2, page=page_num, error_out=True)
  
  # usersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('t_students.html', 
                          title="Administrator", 
                          students=studentsFromDB,
                          colNames=colNames,
                          attributes=attributes)

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

@bp.route('/resolving/task/<task_id>/', methods = ['GET', 'POST'])
def mark_as_resolved(task_id):
  resolve_task = AdminTask.query.get(task_id)
  resolve_task.set_task_as_resolved(True)
  resolve_task.set_task_resolved_on(datetime.datetime.now())
  db.session.add(resolve_task)
  db.session.commit()
  flash("Resolving task successfully")

  return redirect(url_for('myadmin.admin_home'))
