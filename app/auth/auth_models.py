from app import admin
from app import db
from app import login
from flask import redirect
from flask import render_template
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roleType = db.Column(db.String)
    rolelNum = db.Column(db.Integer)
