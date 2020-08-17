from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin




class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  user_fullname = db.Column(db.String(128))
  email = db.Column(db.String(128), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  user_role = db.Column(db.String(10))


  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def set_user_role(self, role):
    self.user_role = role

  def set_username(self, new_name):
    self.username = new_name
  
  def set_user_fullname(self, new_fullname):
    self.user_fullname = new_fullname

  def set_email(self, new_email):
    self.email = new_email

  def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))
  