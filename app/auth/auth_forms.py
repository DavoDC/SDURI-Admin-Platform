from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
import safe

class PasswordReset(FlaskForm):
  email = StringField(
          'Email', 
          validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])
  submit = SubmitField('Reset Password')

  def validate(self):
    initial_validation = super(PasswordReset, self).validate()
    if not initial_validation:
        return False
    user = User.query.filter_by(email=self.email.data).first()
    if not user:
        self.email.errors.append("This email is not registered")
        return False
    return True

class ChangePasswordForm(FlaskForm):
  password = PasswordField(
      'password',
      validators=[DataRequired(), Length(min=6, max=255)]
  )
  confirm = PasswordField(
      'Repeat password',
      validators=[
          DataRequired(),
          EqualTo('password', message='Passwords must match.')
      ]
  )
  
class InitialRegistrationForm(FlaskForm):
  email = StringField('Email', 
                      validators=[DataRequired(message="Email can't be blank"), Email()])
  # role = StringField('Account Type', 
                      # validators=[DataRequired(message="Please select 'Account Type' to proceed")])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')
  

class InitialPasswordNameForm(FlaskForm):
  # Name is also needed, otherwise cannot go to user home page
  # after clicking the login button on login page because
  # username is required as shown in this function [def students(username):]
  # A name should have atleast one letter
  name = StringField('Preferred Name', validators=[DataRequired(), Length(min=1, max=64)]) # [validators.required(), validators.length(min=1)])
  role = StringField('Role', validators=[DataRequired(), Length(min=1, max=64)])
  password = PasswordField(
      'Password',
      validators=[DataRequired(), Length(min=6, max=255)]
  )
  confirm = PasswordField(
      'Repeat password',
      validators=[
          DataRequired(),
          EqualTo('password', message='Passwords must match.')
      ]
  )
