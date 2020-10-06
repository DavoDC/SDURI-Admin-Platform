
# Import modules
from app import app
from app import db
from app import utils
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





# Student user landing page
@app.route('/student/<username>/landing')
@login_required
def students(username):
    return utils.landing_page("Student")


# Student details page
@app.route('/student/<username>/details')
@login_required
def student_details(username):
    rend_temp = render_template('student/details/landing.html',
                                title="Student Details Landing");
    return utils.student_page(rend_temp)


# Student details page series
@app.route('/student/<username>/details/page<int:page_no>',
           methods=['GET', 'POST'])
@login_required
def student_page(username, page_no):

    # Save form data and overwrite
    utils.save_form(username, Student, True)

    # Save files if needed
    flist = ["transcr_file", "eng_file", "cv_file"]
    utils.save_student_files(username, flist)

    # Generate path of question page
    path = 'student/details/pages/page'
    path += str(page_no) + '.html'

    # Base URL
    baseURL = url_for('student_details', username=current_user.name)

    # Render question page,
    # with current and maximum page number
    rend_temp = render_template(path, num=page_no, max=9,
                                baseURL=baseURL,
                                title="Student Details")

    # Render as student page
    return utils.student_page(rend_temp)


# Student explore projects (view or apply)
@app.route('/student/<username>/project/explore')
@login_required
def student_explore(username):

    # Get all projects, ignoring empty/bad rows
    projects = Project.query.filter(Project.title != None).all()

    # Get rendered template
    rend_temp = render_template('student/project/explore.html',
                                title="Explore Projects",
                                projects=projects);

    # Return as student page
    return utils.student_page(rend_temp)


# Student single project
@app.route('/student/<username>/project/single/<int:pid>')
@login_required
def student_single(username, pid):

    # Get project
    project = Project.query.filter_by(id=pid).first() or 404

    # Get student
    student = utils.get_student_from_username(username)

    # Get list of projects applied for (as PIDs)
    pids = utils.get_projects_applied_for(student)
    
    # Can student apply 
    # (Controls if apply button is shown)
    can_apply = False
    
    # If applied for zero or one projects
    numpids = len(pids)
    if numpids == 0 or numpids == 1:
        # The student can (still) apply
        can_apply = True
    
    # Check if this project has been applied for
    applied_for_this = False
    if pid in pids:
        # If already in applied pids, 
        # set to true and cannot apply to this project (again)
        applied_for_this = True
        can_apply = False
    
    # Get rendered template
    rend_temp = render_template('student/project/single.html',
                                title=str(project.title),
                                project=project,
                                can_apply=can_apply,
                                applied_for_this=applied_for_this
                                );

    # Return as student page
    return utils.student_page(rend_temp)


# Student apply for project
@app.route('/student/<username>/project/single/<int:pid>/apply',
           methods=['GET', 'POST'])
@login_required
def student_apply(username, pid):

    # Save form data and overwrite
    utils.save_form(username, Student, True)

    # If data was submitted/saved, go back to project list
    if request.method == "POST":
        return redirect(url_for('project_list', username=username))

    # Get path to HTML
    path = 'student/project/apply.html'

    # Get base URL
    baseURL = url_for('project_apply', username=current_user.name,
                      pid=pid)

    # Get project
    project = Project.query.filter_by(id=pid).first() or 404
    
    # Get title
    title = "Apply for '" + project.title + "'"

    # Slot to save project into
    # (will be 0 if both not free, but this is never used,
    # as apply button is disabled if all slots are filled)
    proj_slot = 0 
    
    # Check slots
    student = utils.get_student_from_username(username)
    one_free = student.proj1_id == None
    two_free = student.proj2_id  == None

    # If first slot is free
    if one_free:
        # Use first slot regardless of second.
        # Applies for (free)(free) and (free)(not_free)
        proj_slot = 1
    elif not one_free and two_free:
        # Else if one is not free but second is
        # i.e. (not_free)(free),
        # use second slot
        proj_slot = 2
    
    # Get preference string
    pref1 = student.proj1_pref
    pref2 = student.proj2_pref
    prefstr = ""
    if(pref1 != None):
        prefstr += pref1
    if(pref2 != None):
        prefstr += pref2

    # Render as one and only page
    rend_temp = render_template(path, num=1, max=1,
                                baseURL=baseURL,
                                title=title,
                                project=project,
                                proj_slot=proj_slot,
                                prefstr=prefstr
                                )

    # Return as student page
    return utils.student_page(rend_temp)


# Student manage project applications
@app.route('/student/<username>/project/manage')
@login_required
def student_manage(username):

    # Get student
    student = utils.get_student_from_username(username)

    # Get list of projects applied for (as PIDs)
    pids = utils.get_projects_applied_for(student)

    # Get projects but only include those applied for
    projects = Project.query.filter(Project.id.in_(pids)).all()

    # Get project 1 details
    proj1 = None
    if(student.proj1_id != None):
        proj1 = [student.proj1_id, student.proj1_pref, student.proj1_dur]
    
    # Get project 2 details
    proj2 = None
    if(student.proj2_id != None):
        proj2 = [student.proj2_id, student.proj2_pref, student.proj2_dur]

    # Get rendered template
    rend_temp = render_template('student/project/manage.html',
                                title="Manage Projects",
                                projects=projects,
                                proj1=proj1, proj2=proj2);

    # Return as student page
    return utils.student_page(rend_temp)








# Supervisor user landing page
@app.route('/supervisor/<username>/landing')
@login_required
def supervisors(username):
    return utils.landing_page("Supervisor")


# Supervisor details (faculty selection page)
@app.route('/supervisor/<username>/details', methods=['GET', 'POST'])
@login_required
def supervisor_details(username):

    # Save form data and overwrite
    utils.save_form(username, Supervisor, True)

    # If data was saved, go back to index
    if request.method == "POST":
        return redirect(url_for('index'))

    # Render as one and only page
    path = 'supervisor/details/faculty-sel.html'
    baseURL = url_for('supervisor_details', username=current_user.name)
    rend_temp = render_template(path, num=1, max=1,
                                baseURL=baseURL,
                                title="Supervisor Details")

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


# Supervisor add project
@app.route('/supervisor/<username>/project/add', methods=['GET', 'POST'])
@login_required
def supervisor_add(username):

    # Save form data but do not overwrite
    utils.save_form(username, Project, False)

    # If data was saved, go back to index
    if request.method == "POST":
        return redirect(url_for('index'))

    # Render as one and only page
    path = 'supervisor/project/add.html'
    baseURL = url_for('add_project', username=current_user.name)
    rend_temp = render_template(path, num=1, max=1,
                                baseURL=baseURL,
                                title="Add Project")

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


# Supervisor manage projects
@app.route('/supervisor/<username>/project/manage', methods=['GET', 'POST'])
@login_required
def supervisor_manage(username):

    # Get current supervisor user_id
    super_id = User.query.filter_by(name=username).first().id or 404

    # Get current supervisor's projects
    cur_user_projects = Project.query.filter_by(user_id=super_id).all()

    return render_template("supervisor/project/edit.html",
                           title="Manage Your Projects",
                           projects=cur_user_projects)


# Supervisor edit project (TEMPORARY)
@app.route('/supervisor/<username>/project/manage/edit', methods=['GET', 'POST'])
@login_required
def supervisor_edit(username):


    # Get current supervisor user_id
    super_id = User.query.filter_by(name=username).first().id or 404

    # Get current supervisor's projects
    cur_user_projects = Project.query.filter_by(user_id=super_id).all()

    return render_template("supervisor/project/edit.html",
                           title="Edit Project",
                           projects=cur_user_projects)

# Logout page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


