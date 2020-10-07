
# Import modules
from app import app
from app import db
from app.helper import utils
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import *
from app.routing import student
from app.routing import supervisor
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from json2html import *

# Main page
@app.route('/')
@app.route('/index')
def index():
    # If user is logged in
    if current_user.is_authenticated:
        # Send to their user page
        return utils.send_to_user_page(current_user.role);

    # Otherwise render normal
    return render_template('index.html', title='Home')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise log in
    # If login form submitted
    form = LoginForm()
    if form.validate_on_submit():

        # Get user
        user = User.query.filter_by(email=form.email.data).first()

        # If user invalid or bad password
        if user is None or not user.check_password(form.password.data):

            # Notify
            flash('Invalid email or password')

            # Send back to login
            return redirect(url_for('login'))

        # Login user
        login_user(user, remember=form.remember_me.data)

        # Send to correct page
        return utils.send_to_user_page(user.role);

    # Render login page
    return render_template('auth/login.html', title='Login', form=form)


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():

    # If user is logged in, send back to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise register
    # If registration form submitted
    form = RegistrationForm()
    if form.validate_on_submit():

        # Create user object
        user = User(name=form.username.data,
                    email=form.email.data)

        # Set password
        user.set_user_password(form.password.data)

        # SIMPLE ROLE SETTING TO BE REPLACED BY MANG
        # Set role according to new user's email
        # If email contains "@uwa.edu.au"
        if "@uwa.edu.au" in user.email:
            # Set user role to "Supervisor"
            user.set_user_role("Supervisor")
        elif "@student.uwa.edu.au" in user.email:
            # Else If email contains "@student.uwa.edu.au"
            # Set user role to "Student"
            user.set_user_role("Student")
        elif "@admin.com" in user.email:
            # Else If email contains "@admin"
            # Set user role to "Administrator"
            user.set_user_role("Administrator")
        else:
            # Else for all other emails
            # Give Student role by default
            user.set_user_role("Student")


        # Add user to database
        db.session.add(user)
        db.session.commit()

        # Notify
        flash('Congratulations, you are now a registered user!')

        # Send to login page
        return redirect(url_for('login'))

    # Show register page
    return render_template('auth/register.html', title='Register', form=form)


# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


