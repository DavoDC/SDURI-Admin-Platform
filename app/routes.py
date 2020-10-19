
# Import modules
from app import app
from app.forms import LoginForm
from app.helper import utils
from app.models import *
from app.models import User
from app.routing import student
from app.routing import supervisor
from flask import flash
from flask import redirect
from flask import render_template
from flask import render_template_string
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
    
    # Check for database file
    dbfile = None
    try:
        # Try to open and close
        dbfile = open("sduri.db", "r")
        dbfile.close()
    except IOError:
        # If database file does not exist
        # Notify
        message = "\nPlease initialize the database first! "
        message += "\n<br>Please use the commands:"
        message += "\n<br>1. 'flask db init'"
        message += "\n<br>2. 'flask db migrate -m \"Creating tables\"'"
        message += "\n<br>3. 'flask db upgrade'"
        message += "\n<br>Ensure that the SDURI.db file is created"
        print(message)
        return render_template_string(message)
       
       
    # Add admin accounts (once)
    utils.add_admin_accounts()
    
    # Add testing accounts
    # DISABLE when not testing!!!
    #utils.add_testing_accounts()
    
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



# Students and supervisors: View project
@app.route('/<role>/<username>/project/manage/view/<int:pid>')
@login_required
def view_project(role, username, pid):

    # Get project
    project = Project.query.filter_by(id=pid).first() or 404

    # Get rendered template
    rend_temp = render_template('templ/view-project.html',
                                title=str(project.title),
                                project=project,
                                role=role
                                );

    # Return page
    return rend_temp



# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


