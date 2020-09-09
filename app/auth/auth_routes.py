from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.auth_forms import PasswordReset
from app.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/forgot_password')
def forgot_password():
  form = PasswordReset()
  return render_template('forgot_password.html', form=form)