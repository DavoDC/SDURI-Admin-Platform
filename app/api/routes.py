from app import controllers
from app import db
from app.api import bp
from app.models import *
from flask import flash
from flask import json
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from json2html import *
from werkzeug.urls import url_parse

# from app import app, db
# The above line is equivalent to
# following two lines after using blue print


@bp.route('/getAllUsers')
# @login_required
def getAllUsers():
    print("Hello")
    users = getAllUsers()
    # return "Hello"
    print("type(users): ", type(users))
    # return json2html.convert(users)
    # return "<pre>json.dumps(users, sort_keys=True, indent=4)</pre>"
    return users
  
    # return json.dumps(json.loads(users), indent=4)

@bp.route('/user_by_id/<int:id>')
def get_user_by_id(id):
    
    user = getUserById(id)
    print(type(user))
    # return user
    print(user.id)
    res = [
        {"id": user.id,
        "name": user.name,
        "email": user.email
        }

    ]
    # return "Hello"
    return jsonify(res)




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
    user = User.query.filter_by(id=userId).first()
  
    if user == None:
        print('Cannot find the user with user id - ', userId)
        return False 
    else:
        return user


def getUserByUsername(username):
    user = User.query.filter_by(name=username).first()
    
    if user == None:
        print('Cannot find the user with username - ', username)
        return False
    else:
        return user
