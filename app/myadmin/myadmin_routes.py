from app import db
from app import email
from app.auth.auth_forms import *
from app.auth.token import *
from app.forms import RegistrationForm
from app.models import *
from app.myadmin import bp
from app.myadmin.myadmin_models import *
import datetime
from datetime import date
from flask import flash
from flask import request


# Returns true if user cannot access admin
def cannot_access_admin():
    return not MyAdminModelView.is_accessible(MyAdminModelView)


# Admin Home
@bp.route('/')
@bp.route('/home')
def admin_home():
    
    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    # templates/myadmin/index.html
    usersFromDB = User.query.all()
    tasks_unresolved = AdminTask.query.filter_by(resolved=False)
    tasks_resolved = AdminTask.query.filter_by(resolved=True)
    return render_template('home.html', title="Administrator",
                           users=usersFromDB, unresolved_tasks=tasks_unresolved,
                           resolved_tasks=tasks_resolved)


# Admin Home: Resolve admin task
@bp.route('/resolving/task/<task_id>/', methods=['GET', 'POST'])
def mark_as_resolved(task_id):
    
    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    resolve_task = AdminTask.query.get(task_id)
    resolve_task.set_task_as_resolved(True)
    resolve_task.set_task_resolved_on(datetime.datetime.now())
    db.session.add(resolve_task)
    db.session.commit()
    flash("Resolving task successfully")
    return redirect(url_for('myadmin.admin_home'))


# Users: Display
@bp.route('/display/users/all/<int:page_num>', methods=['GET', 'POST'])
def display_users(page_num):
    
    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    usersFromDB = User.query.paginate(per_page=10, page=page_num, error_out=True)
    # usersFromDB = user_serializer.dump(userFromDB.items)
    return render_template('users.html', title="Administrator", users=usersFromDB)


# Users: Add
@bp.route('/add/user/', methods=['GET', 'POST'])
def add_user():

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    
    # Get forms
    data = request.form
    form = RegistrationForm()
    
    # If form submitted
    if request.method == 'POST':
   
        # Create account
        user = User(name=data['name'],
                    email=data['email'],
                    confirmed=False,
                    password='password', # Must send password reset email
                    registered_on=date.today(),
                    role=data['role'])
        
        # Add to database
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            acc_msg = "There was an error adding the account to the database"
            acc_msg += ". Email may not be unique"
            flash(acc_msg)
            return redirect(url_for('myadmin.display_users', page_num=1))
        
        # Get token and confirm
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        
        # Notify
        flash("Successfully created user '" + user.name + "'")
        
        # Send password reset email and notify
        try:
            html = render_template('/auth/activate.html', confirm_url=confirm_url)
            subject = ""
            email.send_email(user.email, subject, html)
            flash("Password reset email has been sent to the new user")
        except Exception as e:
            flash("There was an error sending password reset email to user")
        
    return redirect(url_for('myadmin.display_users', page_num=1))


# Users: Update user
@bp.route('/update', methods=['GET', 'POST'])
def update():

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    # Get form
    data = request.form

    # If form submitted
    if request.method == 'POST':

        # Get user and update
        new_data = User.query.get(request.form['id'])
        new_data.name = request.form['name']
        new_data.email = request.form['email']
        new_data.role = request.form['role']

        # Save
        db.session.commit()
        
        # Notify
        flash(new_data.email + "'s information was updated successfully")

    return redirect(url_for('myadmin.display_users', page_num=1))


# Users: Delete user
@bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    # Get user and delete
    del_user = User.query.get(id)
    db.session.delete(del_user)
    
    ### Delete details as well if needed
    # Details row holder
    details_row = None
    # Get user role
    del_role = del_user.role
    # If was student
    if del_role == "Student":
        # Get student details and delete
        details_row  = Student.query.filter_by(user_id=id).first()

    # If was supervisor
    if del_role == "Supervisor":
        # Get supervisor details and delete
        details_row  = Supervisor.query.filter_by(user_id=id).first()

    # If found
    if not details_row is None:
        db.session.delete(details_row)
    
    # Save
    db.session.commit()
    
    # Notify
    msg = "Successfully deleted a user: "
    msg += "'" + del_user.name + ", " + del_user.email + "'"
    msg += " and their details, if any"
    flash(msg)
    
    # Back to users
    return redirect(url_for('myadmin.display_users', page_num=1))



# Students: Display
@bp.route('/display/students/all/<int:page_num>', methods=['GET', 'POST'])
def display_students(page_num):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    col_names = Student.__table__.columns
    colNames = [i.name.upper() for i in col_names] # Capitalize columns' name
    attributes = [i.name for i in col_names] # Columns' name

    # Rearrange colNames as desired, and attributes correspondingly
    fixedCol = [7, 6]
    fixedColNames = [colNames[i] for i in fixedCol]
    fixedColAttributes = [attributes[i] for i in fixedCol]
    colNamesR = colNames[2:6] + colNames[8:]
    attributesR = attributes[2:6] + attributes[8:]
    studentsFromDB = Student.query.paginate(per_page=10, page=page_num, error_out=True)
  
    # usersFromDB = user_serializer.dump(userFromDB.items)
    return render_template('t_students.html', 
                           title="Administrator", 
                           persons=studentsFromDB,
                           colNames=colNamesR,
                           attributes=attributesR,
                           fixedColNames=fixedColNames,
                           fixedColAttributes=fixedColAttributes)

# Students: Edit
@bp.route('/edit/student/', methods=['GET', 'POST'])
def edit_student():

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    

    data = request.form
    col_names = Student.__table__.columns
    # From third column to last column, excluding id and user_id
    colNames = [i.name for i in col_names][2:] # 43 columns at the moment
  
    flash_msg = ""
    if request.method == 'POST':
        new_data = Student.query.get(request.form['id'])
        for column in colNames: # Type of column is string
            if column != "id" or column != "user_id":
                # Convert string to attribute
                setattr(new_data, column, request.form[column])
        db.session.commit()
        flash_msg = new_data.firstname + "'s information was updated successfully"
    flash(flash_msg)
    return redirect(url_for('myadmin.display_students', page_num=1))






# Supervisors: Display
@bp.route('/display/supervisors/all/<int:page_num>', methods=['GET', 'POST'])
def display_supervisors(page_num):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
  
    # Get column names
    col_names = Supervisor.__table__.columns
    colNames = [i.name.upper() for i in col_names] [:] # Uppercase columns' name
    attributes = [i.name for i in col_names][:] # Columns' name

    # Name of all supervisors from user table using user_id
    supervisors = Supervisor.query.all()
    superNames = []
    for supervisor in supervisors: 
        superNames.append((User.query.filter_by(id=supervisor.user_id).first()).name)

    supersFromDB = Supervisor.query.paginate(per_page=10, page=page_num, error_out=True)
    nameDic = {}
    for row in supersFromDB.items:
        nameDic[row.user_id] = User.query.filter_by(id=row.user_id).first().name 
        print(User.query.filter_by(id=row.user_id).first().name)

    return render_template('t_supervisors.html', 
                           title="Administrator", 
                           persons=supersFromDB,
                           colNames=colNames,
                           attributes=attributes,
                           superNames=superNames,
                           nameDic=nameDic)


# Supervisors: Edit supervisor
@bp.route('/edit/supervisor/', methods=['GET', 'POST'])
def edit_supervisor():

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))

    data = request.form
    col_names = Supervisor.__table__.columns
    # From third column to last column, excluding id and user_id
    colNames = [i.name for i in col_names][2:] #
  
    flash_msg = ""
    if request.method == 'POST':
        new_data = Supervisor.query.get(request.form['id'])
        for column in colNames: # Type of column is string
            if column != "id" or column != "user_id":
                # Convert string to attribute
                setattr(new_data, column, request.form[column])
        db.session.commit()
        # flash_msg = new_data.firstname + "'s information is updated successfully"
        flash_msg = "Supervisor information updated successfully"
    flash(flash_msg)
    return redirect(url_for('myadmin.display_supervisors', page_num=1))




# Students and Supervisors: Delete details
@bp.route('/delete/<utype>/<id>/', methods=['GET', 'POST'])
def deleting(utype, id):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))
    
    # Return URL
    retURL = "myadmin.display_"
    
    # If student
    if utype == "Student":
        
        # Get student details and delete
        del_student = Student.query.get(id)
        db.session.delete(del_student)
        
        # Go back to students
        retURL += "students"
    elif utype == "Supervisor":
        
        # Else if supervisor:
        # Get supervisor details and delete
        del_supervisor = Supervisor.query.get(id)
        db.session.delete(del_supervisor)
        
        # Go back to supervisors
        retURL += "supervisors"

    # Save
    db.session.commit()
    
    # Notify
    flash("Successfully deleted a user's details row")
    
    # Back to users ??
    return redirect(url_for(retURL, page_num=1))




# Projects: Display
@bp.route('/display/projects/all/<int:page_num>', methods=['GET', 'POST'])
def display_projects(page_num):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))

    col_names = Project.__table__.columns
    colNames = [i.name.upper() for i in col_names] [:] # Uppercase columns' name
    attributes = [i.name for i in col_names][:] # Columns' name
    print(attributes)
    oriAttributes = attributes # For modaledit_project.html
    colNames = colNames[2:5] + colNames[:2] + colNames[5:]
    attributes = attributes[2:5] + attributes[:2] + attributes[5:]
    projectsFromDB = Project.query.paginate(per_page=10, page=page_num, error_out=True)
  
    # supersFromDB = user_serializer.dump(userFromDB.items)
    return render_template('t_projects.html', 
                           title="Administrator", 
                           persons=projectsFromDB,
                           colNames=colNames,
                           attributes=attributes,
                           oriAttributes=oriAttributes
                           )


# Projects: Edit project
@bp.route('/edit/project/', methods=['GET', 'POST'])
def edit_project():

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))

    data = request.form
    col_names = Project.__table__.columns
    # From third column to last column, excluding id and user_id
    colNames = [i.name for i in col_names][2:] # 
  
    flash_msg = ""
    if request.method == 'POST':
        new_data = Project.query.get(request.form['id'])
        for column in colNames: # Type of column is string
            if column != "id" or column != "user_id":
                # Convert string to attribute
                setattr(new_data, column, request.form[column])
        db.session.commit()
        # flash_msg = new_data.firstname + "'s information is updated successfully"
        flash_msg = "Project information updated successfully"
    flash(flash_msg)
    return redirect(url_for('myadmin.display_projects', page_num=1))


# Projects: Delete project
@bp.route('/delete/project/<int:pid>/', methods=['GET', 'POST'])
def delete_project(pid):

    # If user cannot access admin
    if cannot_access_admin():
        # Send back to index
        return redirect(url_for('index'))

    # Get project to delete
    del_proj = Project.query.get(pid)

    # Delete and save
    db.session.delete(del_proj) 
    db.session.commit()
  
    # Notify
    flash("Successfully deleted a project '" + del_proj.title + "'")

    # Redirect to projects page
    return redirect(url_for('myadmin.display_projects', page_num=1))








