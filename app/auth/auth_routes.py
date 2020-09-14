from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

import datetime
from app import db, email
from app.auth import bp
from app.auth.token import * 
from app.auth.auth_forms import PasswordReset
from app.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/forgot_password')
def forgot_password():
  form = PasswordReset()
  return render_template('forgot_password.html', form=form)

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
  if current_user.confirmed:
    flash('Account already confirmed. Please login.', 'success')
    return redirect(url_for('main.students')) # need to change depending on user
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
  return render_template('/unconfirmed.html')

@bp.route('/resend')
@login_required
def resend_confirmation():
  print("hello")
  return "hello"