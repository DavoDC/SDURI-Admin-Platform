
# Import modules
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import *
from app.models import User
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from json2html import *
import os
from werkzeug.utils import secure_filename

# Unused imports:
#from app import controllers
#from flask import json
#from flask import jsonify
#from werkzeug.urls import url_parse


# Enable favicon support
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Main page
@app.route('/') # methods=['GET', 'POST'])
@app.route('/index') #, methods=['GET', 'POST'])
def index():
    # If user is logged in
    if current_user.is_authenticated:
        # Send to their user page
        return send_to_user_page(current_user.role);

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
        return send_to_user_page(user.role);

    # Render login page
    return render_template('auth/login.html', title='Sign In', form=form)


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

        # Set role according to new user's email
        # If email contains "@uwa.edu.au"
        if "@uwa.edu.au" in user.email:
            # Set user role to "Supervisor"
            user.set_user_role("Supervisor")
        elif "@student.uwa.edu.au" in user.email:
            # Else If email contains "@student.uwa.edu.au"
            # Set user role to "Student"
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


# Helper method: Redirect to user page based on role
def send_to_user_page(role):
    if role == "Administrator":
        return redirect(url_for('admin', username=current_user.name))
    elif role == "Supervisor":
        return redirect(url_for('supervisors', username=current_user.name))
    elif role == "Student":
        return redirect(url_for('students', username=current_user.name))
    else:
        msg = "Unknown role in function 'send_to_user_page'"
        msg += "\n<br>This means your account has no role set"
        msg += "\n<br>Look at register() code / Change email domain"
        print(msg)
        return msg


# Admin user page
@app.route('/admin/<username>')
@login_required
def admin(username):
    user = User.query.filter_by(name=username).first_or_404()
    users = User.query.all()
    return render_template('admin/admin.html',
                           user=user, title='Admin', users=users)


# Supervisor user page
@app.route('/supervisor/<username>')
@login_required
def supervisors(username):
    
    # If user role is not supervisor
    if current_user.role != "Supervisor":
        
        # Send back to index
        return redirect(url_for('index'))
    
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('supervisor/supervisors.html',
                           user=user, title='Supervisor')


# Supervisor faculty choice page
@app.route('/supervisor/<username>/details')
@login_required
def supervisor_faculty(username):

    return render_template('supervisor/details.html')


# Student user page
@app.route('/students/<username>') 
@login_required
def students(username):
  
    # If user role is not student
    if current_user.role != "Student":
        
        # Send back to index
        return redirect(url_for('index'))
    
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('student/students.html',
                           user=user, title='Student')


# Student details page
@app.route('/students/<username>/details')
@login_required
def student_details(username):
    return render_template('student/details/landing.html');


# Questions routing for student details question series
@app.route('/students/<username>/details/page<int:page_no>',
           methods=['GET', 'POST'])
@login_required
def question(username, page_no):

    # Generate path of question page
    url = 'student/details/pages/page'
    url += str(page_no) + '.html'

    # Get current student user_id
    cs_id = User.query.filter_by(name=username).first().id or 404

    # Get current student
    cur_student = Student.query.filter_by(user_id=cs_id).first()

    # If there is no database row
    if not Student.query.filter_by(user_id=cs_id).first():

        # Initialize row and commit
        db.session.add(Student(cs_id))
        db.session.commit()

    # If mode is post
    if request.method == "POST":

        # Using "request" module, which is imported from the flask at the top,
        # this line gets all html form attributes: name and user input text
        # e.g. <input name="sample_name">user_input_text in a box or anything
        # The variable "data" stores name and user_input_text in dictionary format
        data = request.form

        # The values of name attributes in html form, sample_name above in this case,
        # must be same with the names of columns in the database.
        for column_name, input_text in data.items():
            
            # Inserting data into the remaining columns of Student table
            setattr(cur_student, column_name, input_text)
            
        # Save files if needed
        save_file("eng_file", cur_student)
        save_file("cv_file", cur_student)
        save_file("transcr_file", cur_student)
        
        # Commit to database
        db.session.commit()

    # Render question page,
    # with current and maximum page number
    return render_template(url, num=page_no, max=9)


# Helper method: 
# - Save file to static if it exists
# - Add filename to database
def save_file(file_field_name, cur_student):
    
    # For every file in form data matching field
    # (Note: This way is best, tries to get from wrong page otherwise)
    for uploaded_file in request.files.getlist(file_field_name):

        # Get secure filename
        filename = secure_filename(uploaded_file.filename)

        # If filename is not empty
        if filename != '':

            # Save file to path
            path = "app/static/user-files"
            uploaded_file.save(os.path.join(path, filename))

            # Save file name in database
            setattr(cur_student, file_field_name, filename)

# Project list (draft)
@app.route('/project_list')
def project_list():
    return render_template('project/project-list.html', title='Project list')

# Single project (draft)
@app.route('/project_list/single_project')
def single_project():
    path = "project/single-project.html"
    if current_user.is_authenticated:
        return render_template(path, title='Project specifics', 
                               logged=True)
    else:
        return render_template(path, title='Project specifics', 
                               logged=False)
                               
# Student apply for project (draft)
@app.route('/project_list/single_project/apply')
def single_project_apply():
    return render_template("student/apply-for-project.html");

# Supervisor add project (draft)
@app.route('/add-project')
def add_project():
    return render_template("supervisor/add-project.html");

# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


