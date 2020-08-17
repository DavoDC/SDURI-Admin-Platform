from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app import app
# from app.forms import Login, Registration, AdminAddAccount, ChangePassword, SubAddQuestion, AdminAddQuestions, AdminAddQuiz, MainFormOptions, SubFormQuestion, SubAddOption
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException, Forbidden
from functools import wraps
# from app.controllers.UserController import UserController
# from app.controllers.QuizController import QuizController, QuestionType
# from app.controllers.QuizAttemptController import QuizAttemptController
from datetime import datetime
import json

@app.route('/')
@app.route('/index')
def landing_page():
    # return "Hello"
    return render_template("landing-page.html", title="Welcome")