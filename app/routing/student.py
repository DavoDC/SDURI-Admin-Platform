
# Import modules
from app import app
from app.helper import utils
from app.models import *
from app.routing import *
from flask import render_template
from flask import request
from flask_login import login_required
from json2html import *


## Student user landing page
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
    rend_temp = render_template('student/project/explore/explore.html',
                                title="Explore Projects",
                                projects=projects);

    # Return as student page
    return utils.student_page(rend_temp)



# Student select project
@app.route('/student/<username>/project/select/<int:pid>')
@login_required
def student_select(username, pid):

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
    rend_temp = render_template('student/project/explore/select.html',
                                title=str(project.title),
                                project=project,
                                can_apply=can_apply,
                                applied_for_this=applied_for_this
                                );

    # Return as student page
    return utils.student_page(rend_temp)



# Student apply for project
@app.route('/student/<username>/project/select/<int:pid>/apply',
           methods=['GET', 'POST'])
@login_required
def student_apply(username, pid):

    # Save form data and overwrite
    utils.save_form(username, Student, True)

    # If data was submitted/saved, go back to project list
    if request.method == "POST":
        return redirect(url_for('student_explore', username=username))

    # Get path to HTML
    path = 'student/project/explore/apply.html'

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
    proj1 = utils.get_proj1_details(student)

    # Get project 2 details
    proj2 = utils.get_proj2_details(student)

    # Get rendered template
    rend_temp = render_template('student/project/manage/manage.html',
                                title="Manage Projects",
                                projects=projects,
                                proj1=proj1,
                                proj2=proj2);

    # Return as student page
    return utils.student_page(rend_temp)


# Student unapply for project
@app.route('/student/<username>/project/manage/unapply/<int:pid>',
           methods=['GET', 'POST'])
@login_required
def student_unapply(username, pid):

    # Get user type id
    ut_id = User.query.filter_by(name=username).first().id or 404

    # If data was submitted/saved
    if request.method == "POST":

        # Get dictionary of data linked to 'name' attributes
        data = request.form

        # Get existing row
        row = Student.query.filter_by(user_id=ut_id).first()
            
        # For each name-data pair
        for name_attr, input_data in data.items():

            # Set attribute to None
            setattr(row, name_attr, None)
            
        # Commit to database
        db.session.commit()
        
        # Go back 
        return redirect(url_for('student_manage', username=username))
    
    # Get project
    project = Project.query.filter_by(id=pid).first() or 404
    
    # Get title
    title = "Unapply for '" + str(project.title) + "'"
    
    # Get student
    student = utils.get_student_from_username(username)
    
    # Get slot to remove
    proj_slot = None
    if pid == student.proj1_id:
        proj_slot = 1
    elif pid == student.proj2_id:
        proj_slot = 2

    # Render as one and only page
    path = 'student/project/manage/unapply.html'
    rend_temp = render_template(path, num=1, max=1,
                                title=title,
                                project=project,
                                proj_slot=proj_slot
                                )

    # Return as student page
    return utils.student_page(rend_temp)

