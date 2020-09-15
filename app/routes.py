from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.decorators import * # check_confirmed
from . import email
from app.auth.token import generate_confirmation_token, confirm_token
from datetime import date
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from json2html import *
from app import app, db, mail
from app.forms import LoginForm, RegistrationForm
from app.models import *
from app import controllers

@app.route('/') # methods=['GET', 'POST'])
@app.route('/index') #, methods=['GET', 'POST'])
# @login_required
def index():  
  return render_template('index.html', title='Home')

@app.route('/admin/<username>')
@login_required
def admin(username):
  user = User.query.filter_by(name=username).first_or_404()
  users = User.query.all()
  return render_template('admin.html', user=user, title='Admin', users=users)

@app.route('/supervisor/<username>')
@login_required
def supervisors(username):
  user = User.query.filter_by(name=username).first_or_404()
  return render_template('supervisors.html', user=user, title='Supervisor')

@app.route('/students/<username>/home', methods=['GET', 'POST'])
@login_required
@check_confirmed
def students(username):
  if request.method == "POST":
    # For dynamic url, pass this "username=current_user.name" 
    # argument to redirect(url_for()) function below
    return redirect(url_for('questions', question_page_no=1, username=current_user.name))
  return render_template('students.html', title='Student')

@app.route('/students/<username>/q/<int:question_page_no>', methods=['GET', 'POST'])
@login_required
def questions(username, question_page_no):
  # page number starts from 1
  current_question_page_no = question_page_no

  # constructing filename for next page
  html_file = "q_p" + str(current_question_page_no) + ".html"

  # cs_id = current student user_id
  cs_id = User.query.filter_by(name=username).first().id or 404
  current_student = Student.query.filter_by(user_id=cs_id).first()
  if not Student.query.filter_by(user_id=cs_id).first():
    # Inserting user_id into Student table
    # and leaving other columns empty
    db.session.add(Student(cs_id, "","",""))
    db.session.commit()

  if request.method == "POST":
    # Using "request" module, which is imported from the flask at the top,
    # this line gets all html form attributes: name and user input text
    # e.g. <input name="sample_name">user_input_text in a box or anything
    # The variable "data" stores name and user_input_text in dictionary format
    data = request.form 

    # The values of name attributes in html form, sample_name above in this case,
    # must be same with the names of columns in the database.
    for column_name, input_text in data.items():
      # Inserting data into the remaining columns of Student table
      setattr(current_student, column_name, input_text)
    db.session.commit()
    
    # Total number of html files containing questions for students
    # Change the integer 9 to the number of pages available
    total_num_page = 9 
    if current_question_page_no < total_num_page:
      # In order to go to the next page we need to increase
      # questions page number
      current_question_page_no += 1
    return redirect(url_for('questions', 
                            question_page_no=current_question_page_no, 
                            username=current_user.name
                            )
                    )
  return render_template(html_file, title='Student')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid email or password')
      return redirect(url_for('login'))
  
    
    
    login_user(user, remember=form.remember_me.data)
    # may need to change use.confirmed to current_user.confirmed 
    if user.confirmed == False:
      flash('Your accounnt has not been activated...\nPlease check your email.', 'success')
      # unconfirmed_name = unconfirmed username; unconfirmed_email = unconfirmed user email
      return redirect(url_for('auth.unconfirmed', unconfirmed_name=user.name, unconfirmed_email=user.email))
    # next_page = request.args.get('next')
    # if not next_page or url_parse(next_page).netloc != '':
    #   next_page = url_for('index')
    # return redirect(next_page)
    # return redirect(url_for('index.html')) # Use if next_page or next variable is not used
    if user.role == "Administrator":
      return redirect(url_for('admin', username=current_user.name))
    elif user.role == "Supervisor":
      return redirect(url_for('supervisors', username=current_user.name))
    else:
      return redirect(url_for('students', username=current_user.name))
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user()
  flash('You were logged out.', 'success')
  return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(name=form.username.data,  
                # user_fullname=form.user_fullname.data,
                email=form.email.data,
                confirmed=False,
                password=form.password.data,
                registered_on=date.today())
    
    # If new user's email contains "@uwa.edu.au" 
    # then set user role to "Supervisor"
    if "@uwa.edu.au" in user.email:
      user.set_user_role("Supervisor")
    
    # user.set_user_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('/auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    email.send_email(user.email, subject, html)
    
    login_user(user)
    flash('A confirmation email has been sent to your email.', 'success')    
    flash('Congratulations, you are now a registered user!', 'con_reg_user')
    
    return redirect(url_for('auth.unconfirmed'))
  return render_template('register.html', title='Register', form=form)











