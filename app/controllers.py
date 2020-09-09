from app.models import *
from app import db

from flask import render_template, flash, redirect, url_for, Markup, current_app
from flask_login import login_required, current_user, login_user, logout_user
import sys
from datetime import datetime
import operator as o

def getAllUsers():
  user = User.query.all()
  return user

def getUserById(userId):
  print("userId: ", userId)
  user = User.query.filter_by(id=userId).first()
  if user==None:
    print('cannot find the user with user id - ', userId)
    return False 
  else:
    return user

def getUserByUsername(username):
  user = User.query.filter_by(name=username).first()
  if user==None:
    print('cannot find the user with username - ', username)
    return False
  else:
    return user
