from app import db, admin, login
from flask import redirect, render_template, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class Roles(db.Model):
  __tablename__ = 'roles'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roleType = db.Column(db.String)
  rolelNum = db.Column(db.Integer)
<<<<<<< HEAD
  
=======
>>>>>>> 23eb4ff3ffa694f4f762cd4b6d07e34dbe83893b
