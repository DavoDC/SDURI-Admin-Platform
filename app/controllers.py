from app.models import *
from app import db
from sqlalchemy import inspect
from sqlalchemy_utils.functions.orm import get_column_key

from flask import render_template, flash, redirect, url_for, Markup, current_app, jsonify, json
from flask_login import login_required, current_user, login_user, logout_user
import sys
from datetime import datetime
import operator as o

def getAllUsers():
  users = User.query.all()
  result = []
  for user in users:
    dic = {column.name: getattr(user, column.name) 
          for column in User.__table__.columns
          if column.name != 'password'}
    # print("dic: ", dic)
    result.append(dic)

  print("result: ", json.dumps(result, indent=4))
  return jsonify(result)


def getUserById(userId):
  # print("userId: ", userId)
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
