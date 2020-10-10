
# Import modules
from app import db
from app.models import *
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from json2html import *
import os
from werkzeug.utils import secure_filename


# Redirect to user page based on role
def send_to_user_page(role):
    if role == "Administrator":
        return redirect(url_for('myadmin.admin_home', username=current_user.name))
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


# Render student pages
def student_page(rend_temp_path):
    return user_page("Student", rend_temp_path)

# Render supervisor pages
def supervisor_page(rend_temp_path):
    return user_page("Supervisor", rend_temp_path)

# Render user page so that only users with correct role can see it
def user_page(role, rend_temp):

    # If current user role doesn't match input role
    if current_user.role != role:

        # Send back to index
        return redirect(url_for('index'))

    # Else if role is correct,
    # render template
    return rend_temp


# Return true if student details are good
def are_stud_det_good(username):
    
    # Get student and make new row if needed
    student = get_user_from_username(username, Student, True)
    
    # check first few first, then do full check
    
    # TODO
    return True



# Get user ID from username
def get_uid_from_name(username):
    
    # Get user id
    uid = User.query.filter_by(name=username).first().id or 404
    
    # If user id was not found
    if uid == 404:
        # Notify
        raise ValueError('User ID not found (utils.py)')
    
    # Otherwise return
    return uid


# Get project from id
def get_project_from_id(pid):
    
    # Get project
    project = Project.query.filter_by(id=pid).first() or 404
    
    # If project was not found
    if project == 404:
        # Notify
        raise ValueError('Project not found (utils.py)')
    
    # Otherwise return
    return project
    


# Add empty row to database
def add_empty_row(username, custDB):
    
    # Get UID
    uid = get_uid_from_name(username)
    
    # If there is no database row
    if not custDB.query.filter_by(user_id=uid).first():

        # Initialize row and commit
        db.session.add(custDB(uid))
        db.session.commit()



# Save form data into given DB
def save_form(username, custDB, overwrite):

    # If we are not overwriting
    if not overwrite:
        # We are adding a new row
        add_empty_row(username, custDB)

    # If mode is post
    if request.method == "POST":

        # Get dictionary of data linked to 'name' attributes
        data = request.form

        # Get row
        row = None
        
        # Get user ID
        uid = get_uid_from_name(username)
        
        # If overwrite is on
        if overwrite:
            # Get existing row
            row = custDB.query.filter_by(user_id=uid).first()
        else:
            # Else if overwrite is off,
            # make a new row
            row = custDB(uid)

        # For each name-data pair
        for name_attr, input_data in data.items():

            # Update database row,
            # matching name attribute to the column name
            setattr(row, name_attr, input_data)
            
        # If overwrite off
        if not overwrite:
            # Add new row
            db.session.add(row)

        # Commit to database
        db.session.commit()



# Save student files
def save_student_files(username, file_fields):

    # If mode is post
    if request.method == "POST":

        # Get student
        student = get_student_from_username(username)

        # For all files
        for ff_name in file_fields:

            # Save file
            save_file(ff_name, student)



# Save file to static if it exists and add filename to database
def save_file(file_field_name, student):

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
            setattr(student, file_field_name, filename)

            # Commit to database
            db.session.commit()


# Get list of projects applied for (as PIDs)
def get_pids_applied_for(student):
    
    # Define empty list
    pids = []
    
    # Get first pid
    first = student.proj1_id
    
    # If first pid is valid
    if first != None:
        
        # Add to list
        pids.append(first)
    
    # Get second pid
    second = student.proj2_id
    
    # If second pid is valid
    if second != None:
        
        # Add to list
        pids.append(second)
        
    # Return list
    return pids

        
# Get user row with given username from given user database
# - do_init: If true, create row if not found
def get_user_from_username(username, userDB, do_init):
    
    # Get UID
    uid = get_uid_from_name(username)
    
    # Get user from username
    user = userDB.query.filter_by(user_id=uid).first() or 404
    
    # If student doesn't exist
    if user == 404:
        
        # If init is on
        if do_init:
        
            # Add empty row
            add_empty_row(username, userDB)

            # Retrieve again (but no init will be needed)
            return get_user_from_username(username, userDB, False)
        else:
            # Else notify
            raise ValueError('User not found (utils.py)')
    
    # Return user
    return user

    
# Get project 1 details triplet
def get_proj1_details(student):

    # Get id
    pid = student.proj1_id
    
    # Check if valid
    if(pid == None):
        return None

    # Get preference
    pref = student.proj1_pref
        
    # Get duration
    dur = student.proj1_dur
    
    # Return triplet
    return [pid, pref, dur]


# Get project 2 details triplet
def get_proj2_details(student):

    # Get id
    pid = student.proj2_id
    
    # Check if valid
    if(pid == None):
        return None

    # Get preference
    pref = student.proj2_pref
        
    # Get duration
    dur = student.proj2_dur
    
    # Return triplet
    return [pid, pref, dur]
    
    
# Convert row to dictionary
def get_row_as_dict(row):
    
    # Get project values dictionary
    row_dict = row.__dict__
    
    # Remove unneeded pair
    row_dict.pop('_sa_instance_state')
    
    # For each key in row
    for key in row_dict:
        
        # If None, make empty string
        if row_dict[key] is None:
            row_dict[key] = ""
          
    # Return
    return row_dict


# Get supervisor's projects from username
def get_supervisors_projects(username):
    
    # Get ID
    sid = get_uid_from_name(username)
    
    # Return their projects that are initialized
    return Project.query.filter_by(user_id=sid).filter(Project.title != None).all()