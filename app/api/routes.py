from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from json2html import *
# from app import app, db
# The above line is equivalent to
# following two lines after using blue print
from app import db
from app.api import bp
from app.models import *
from app import controllers


@bp.route('/getAllUsers')
# @login_required
def getAllUsers():
  print("Hello")
  users = controllers.getAllUsers()
  # return "Hello"
  print("type(users): ", type(users))
  # return json2html.convert(users)
  # return "<pre>json.dumps(users, sort_keys=True, indent=4)</pre>"
  return users
  
  # return json.dumps(json.loads(users), indent=4)

@bp.route('/user_by_id/<int:id>')
def get_user_by_id(id):
    
    user = controllers.getUserById(id)
    print(type(user))
    # return user
    print(user.id)
    res = [
        {"id" : user.id,
        "name" : user.name,
        "email" : user.email
        }

    ]
    # return "Hello"
    return jsonify(res)
