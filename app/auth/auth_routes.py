from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

import datetime
from app import db, email
from app.auth import bp

from app.auth.token import * # generate_confirmation_token, confirm_token 
from app.auth.auth_forms import * # PasswordReset, ChangePasswordForm, InitialPasswordNameForm
<<<<<<< HEAD
=======
from app.forms import LoginForm, RegistrationForm
>>>>>>> 23eb4ff3ffa694f4f762cd4b6d07e34dbe83893b
from app.forms import LoginForm, RegistrationForm
from app.models import *
from app.routes import *
from app.myadmin.myadmin_models import *


@bp.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
  form = PasswordReset(request.form)
  pwChangeForm = ChangePasswordForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    token = generate_confirmation_token(user.email)
    
    user.password_reset_token = token
    db.session.commit()

    reset_url = url_for('auth.reset_password', token=token, _external=True)
    html = render_template('auth/pwreset_msg.html',
                          username=user.email,
                          reset_url=reset_url)
    subject = "Reset your password"
    email.send_email(user.email, subject, html)

    flash('A password reset email has been sent via email.', 'success')
    return redirect(url_for("index"))
  return render_template('forgot_password.html', form=form)

@bp.route('/password/forgot/new/<token>', methods=['GET', 'POST'])
def reset_password(token):
  form = ChangePasswordForm(request.form)
  email = confirm_token(token)
  user = User.query.filter_by(email=email).first_or_404()

  if user.password_reset_token is not None:
    # form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
      user = User.query.filter_by(email=email).first()
      if user:
        user.password = generate_password_hash(form.password.data)
        user.password_reset_token = None
        db.session.commit()

        login_user(user)

        print("flash('Password successfully changed.', 'success')")
        # return redirect(url_for('user.profile'))
        return redirect(url_for('students', username=current_user.name))
    

      # else:
        flash('Password change was unsuccessful.', 'danger')
      #   # return redirect(url_for('auth.profile'))
        return redirect(url_for('students', username=current_user.name))
        
    else:
      flash('You can now change your password.', 'success')
      return render_template('auth/reset_password.html', form=form)
  else:
    flash('Can not reset the password, try again.', 'danger')

  return redirect(url_for('index'))
  

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
  if current_user.confirmed:
    flash('Account already confirmed. Please login.', 'success')
    return redirect(url_for('students', username=current_user.name)) # need to change depending on user
  email = confirm_token(token)
  user = User.query.filter_by(email=current_user.email).first_or_404()
  if user.email == email:
    user.confirmed = True
    user.confirmed_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    flash('You have confirmed your account. Thanks!', 'success')
  else:
    flash('The confirmation link is invalid or has expired.', 'danger')
  # return redirect(url_for('main.students')) # return for other user types
  return redirect(url_for('index'))

@bp.route('/unconfirmed', methods=['GET', 'POST'])
def unconfirmed():
  return render_template('unconfirmed.html')

@bp.route('/resend')
@login_required
def resend_confirmation():
  # email = request.args.get('unconfirmed_email')

  # token = generate_confirmation_token(use.email)
  token = generate_confirmation_token(current_user.email)
  print("...user.email " , current_user.email)
  confirm_url = url_for('auth.confirm_email', token=token, _external=True)
  html = render_template('/auth/activate.html', confirm_url=confirm_url)
  subject = "Please confirm your email"
  # this user.email may to be changed to current_user.email
  # email.send_email(user.email, subject, html)
  email.send_email(current_user.email, subject, html)
  flash('A new confirmation email has been sent.', 'success')
  return redirect(url_for('auth.unconfirmed'))

@bp.route('/initial-pwd-setting/<token>', methods=['GET', 'POST'])
def initial_pwd_setting(token):
  """Confirm email and set password for the first time"""
  roles = ["Student", "Supervisor"]
  form = InitialPasswordNameForm()
  # Get email from the token
  email_fr_token = confirm_token(token)
  print("email_fr_token: ", email_fr_token)
  # user = User.query.filter_by(email=current_user.email).first_or_404()
  user = User.query.filter_by(email=email_fr_token).first_or_404()
  # if user.email == email_fr_token:

  flash_msg = "" # flash message
  flash_msg_cat = "" # flash message category
  # If a supervisor uses email that does not contain 
  # "@uwa.edu.au" confirmation is required from administrator
  confirmed_required = False
  if form.validate_on_submit():
    if user: # Double checking user object from above
      # By default, user.role is "Student" except for
      # users' email that contains "@uwa.edu.au"
      # This condition checks if someone wants to be 
      # a supervisor but not using an email that
      # does not contain "@uwa.edu.au"
      if user.role != form.role.data and \
        form.role.data == "Supervisor":
        # Request confirmation from administrator
        confirmed_required = True
        flash_msg = 'Action required: Administrator confirmation'
        flash_msg_cat = 'warning'
        # Change this code below
        # Send notification to admin email or 
        # task list on home page
        # pass
        
        t_description = "Check users who are waiting for your confirmation"
        t_action = "Confirm user's role"
        task = AdminTask( description=t_description,
                          action=t_action,
                          userEmail=email_fr_token)
        db.session.add(task)
        db.session.commit()

      else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        flash_msg = 'Password setting successfully completed.'
        flash_msg_cat = 'success'

    user.set_user_name(form.name.data)
    user.set_user_password(form.password.data)
    user.password_reset_token = None
    db.session.commit()
      

      
    flash(flash_msg, flash_msg_cat)
    print(flash_msg)
    return render_template('index.html')
  
  # Need to get password and name, otherwise cannot go to user home page
  # after clicking the login button on login page because
  # username is required as shown in this function [def students(username):]
  return render_template('/auth/initial_pwd_name.html', form=form, roles=roles)
