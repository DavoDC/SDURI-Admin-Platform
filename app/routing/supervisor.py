
# Import modules
from app import app
from app.helper import utils
from app.models import *
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from json2html import *

# Supervisor user landing page
@app.route('/supervisor/<username>/landing')
@login_required
def supervisors(username):
    
    # Get supervisor
    sv = utils.get_user_from_username(username, Supervisor, True)
    
    # Check if details are good
    good_det = sv.faculty != None and sv.school != None
    
    # Render template
    rend_temp = render_template("supervisor/landing.html", 
                                title="Supervisor Landing",
                                good_det=good_det)
 
    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


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
                                title="Supervisor Details"
                                )

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
    baseURL = url_for('supervisor_add', username=username)
    rend_temp = render_template(path, num=1, max=1,
                                baseURL=baseURL,
                                title="Add Project")

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


# Supervisor manage projects
@app.route('/supervisor/<username>/project/manage', methods=['GET', 'POST'])
@login_required
def supervisor_manage(username):

    # Get supervisors projects
    projects = utils.get_supervisors_projects(username)
        
    # Render
    rend_temp = render_template("supervisor/project/manage/manage.html",
                                title="Manage Your Projects",
                                projects=projects)

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


# Supervisor edit project
@app.route('/supervisor/<username>/project/manage/edit/<int:pid>',
           methods=['GET', 'POST'])
@login_required
def supervisor_edit_project(username, pid):

    # If mode is post
    if request.method == "POST":

        # Get dictionary of data linked to 'name' attributes
        data = request.form
        
        # Get user ID
        uid = utils.get_uid_from_name(username)
        
        # Get existing row for supervisor's specific project!
        row = Project.query.filter_by(user_id=uid).filter(Project.id == pid).first()

        # For each name-data pair
        for name_attr, input_data in data.items():

            # Update database row,
            # matching name attribute to the column name
            setattr(row, name_attr, input_data)

        # Commit to database
        db.session.commit()
        
        # Return to manage projects
        return redirect(url_for('supervisor_manage', username=username))
    
    # Get project as dictionary
    project = utils.get_project_from_id(pid)
    proj_dict = utils.get_row_as_dict(project, True)

    # Render as one and only page
    path = "supervisor/project/manage/edit.html"
    baseURL = url_for('supervisor_edit_project', 
                      username=username, pid=pid)
    rend_temp = render_template(path, num=1, max=1,
                                baseURL=baseURL,
                                title="Edit Project",
                                proj_dict=proj_dict)

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)




# Supervisor manage applications
@app.route('/supervisor/<username>/project/manage/view/appl/<int:pid>')
@login_required
def supervisor_view_appl(username, pid):

    # Get supervisors projects
    projects = utils.get_supervisors_projects(username)
    
    # Studients applied
    students = []
    
    # Get students that have applied for at least one project
    studentsTemp = Student.query.filter((Student.proj1_id != None) | (Student.proj2_id != None)).all()

    # For every student that has selected at least one project
    for student in studentsTemp:
        # For all project ids
        projects = utils.get_pids_applied_for(student)
        if pid in projects:
            # If this project is the student's 1st pref
            if student.proj1_id == pid:
                # If this project's accept status is pending, then show the application, else ignore the student
                if student.proj1_accepted is "Pending":
                    students.append(student)
            
            # Do the same for the student's 2nd pref
            if student.proj2_id == pid:
                # If this project's accept status is pending, then show the application, else ignore the student
                if student.proj2_accepted is "Pending":
                    students.append(student)

    # Get columns
    col_names = Student.__table__.columns 
    colNames = [i.name.capitalize() for i in col_names]
    attributes = [i.name for i in col_names] 
    
    # make list of cols to remove, do forloop
    # Remove irrelevant project slot
    # Remove emergency details
    # Remove columns
    colNames.remove('Id')
    attributes.remove('id')
    colNames.remove('User_id')
    attributes.remove('user_id')
    
    # Render
    rend_temp = render_template("supervisor/project/manage/view-appl.html",
                                title="View Applications",
                                students=students,
                                colNames=colNames,
                                attributes=attributes,
                                pid=pid)

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)


# Supervisor examine student details
@app.route('/supervisor/<username>/project/manage/view/appl/<pid>/<student_id>')
@login_required
def supervisor_examine(username, pid, student_id):

    this_student = Student.query.filter_by(id=student_id).first()

    # Render
    rend_temp = render_template("supervisor/project/manage/examine.html", title="Examine student details", pid=pid, sid=student_id, this_student=this_student)

    # Render as supervisor page
    return utils.supervisor_page(rend_temp)

# Accept
@app.route('/accept/<sid>/<pid>')
@login_required
def accept(sid, pid):

    # get the student object
    this_student = Student.query.filter_by(id=sid).first()

    # if current project is project 1
    if this_student.proj1_id == pid:
        this_student.proj1_accepted = "Accepted"
        db.session.commit()
    else:
        this_student.proj2_accepted = "Accepted"
        db.session.commit()

    return redirect(url_for('index'))

# Deny
@app.route('/deny/<sid>/<pid>')
@login_required
def deny(sid, pid):

    # get the student object
    this_student = Student.query.filter_by(id=sid).first()

    # if current project is project 1
    if this_student.proj1_id == pid:
        this_student.proj1_accepted = "Denied"
        db.session.commit()
    else:
        this_student.proj2_accepted = "Denied"
        db.session.commit()

    return redirect(url_for('index'))
