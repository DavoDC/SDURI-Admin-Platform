from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class PasswordReset(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Reset Password')
