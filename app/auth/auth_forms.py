from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

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
