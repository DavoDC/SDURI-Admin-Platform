
from app.models import *
from flask import json
from flask import jsonify

# Unused imports:
#from datetime import datetime
#from flask import Markup
#from flask import current_app
#from flask import flash
#from app import db
#from flask import redirect
#from flask import render_template
#from flask import url_for
#from flask_login import current_user
#from flask_login import login_required
#from flask_login import login_user
#from flask_login import logout_user
#import operator as o
#from sqlalchemy import inspect
#from sqlalchemy_utils.functions.orm import get_column_key
#import sys

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
  
    if user == None:
        print('cannot find the user with user id - ', userId)
        return False 
    else:
        return user

def getUserByUsername(username):
    user = User.query.filter_by(name=username).first()
    if user == None:
        print('cannot find the user with username - ', username)
        return False
    else:
        return user
