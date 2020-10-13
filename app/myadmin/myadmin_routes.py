from app import db
from app import email
from app.auth.auth_forms import *
from app.auth.token import *
from app.forms import RegistrationForm
from app.models import *
from app.myadmin import bp
from app.myadmin.myadmin_models import *
import datetime
from flask import flash
from flask import request

@bp.route('/home') #, methods=['GET', 'POST'])
@bp.route('/')
def admin_home():
    # templates/myadmin/index.html
    usersFromDB = User.query.all()
    tasks_unresolved = AdminTask.query.filter_by(resolved=False)
    tasks_resolved = AdminTask.query.filter_by(resolved=True)
    return render_template('home.html', title="Administrator",
                           users=usersFromDB, unresolved_tasks=tasks_unresolved,
                           resolved_tasks=tasks_resolved)

@bp.route('/update', methods=['GET', 'POST'])
def update():
    # request.form = ImmutableMultiDict([('id', '2'), ('name', 'supervisor111'), ('email', 'super1@supers.com')])
    # type(request.form) = <class 'werkzeug.datastructures.ImmutableMultiDict'>
    # The tuples' values can be accessed in this format: request.form['id']
    data = request.form
    flash_msg = ""
    if request.method == 'POST':

        # new_data = User.query.filter_by(id=update_id)
        new_data = User.query.get(request.form['id'])
        print("new_data: ", new_data)
        new_data.name = request.form['name']
        new_data.email = request.form['email']
        new_data.role = request.form['role']

        db.session.commit()
        flash_msg = new_data.email + "'s information is updated successfully"
    flash(flash_msg)
    # return render_template('home.html', user)
    return redirect(url_for('myadmin.display_users', page_num=1))


@bp.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    del_user = User.query.get(id)
    db.session.delete(del_user)
    db.session.commit()
    flash("Successfully deleted a user '" + del_user.email + "'")
    return redirect(url_for('myadmin.display_users', page_num=1))


@bp.route('/display/users/all/<int:page_num>', methods=['GET', 'POST'])
def display_users(page_num):
    usersFromDB = User.query.paginate(per_page=2, page=page_num, error_out=True)
    # usersFromDB = user_serializer.dump(userFromDB.items)
    return render_template('users.html', title="Administrator", users=usersFromDB)


@bp.route('/display/projects/all/<int:page_num>', methods=['GET', 'POST'])
def display_projects(page_num):
  col_names = Project.__table__.columns
  colNames = [i.name.upper() for i in col_names] [:] # Uppercase columns' name
  attributes = [i.name for i in col_names][:] # Columns' name
  print(attributes)
  oriAttributes = attributes # For modaledit_project.html
  colNames = colNames[2:5] + colNames[:2] +colNames[5:]
  attributes = attributes[2:5] + attributes[:2] +attributes[5:]
  projectsFromDB = Project.query.paginate(per_page=2, page=page_num, error_out=True)
  
  # supersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('t_projects.html', 
                          title="Administrator", 
                          persons=projectsFromDB,
                          colNames=colNames,
                          attributes=attributes,
                          oriAttributes=oriAttributes
                          )

@bp.route('/edit/project/', methods=['GET', 'POST'])
def edit_project():
  data = request.form
  col_names = Project.__table__.columns
  # From third column to last column, excluding id and user_id
  colNames = [i.name for i in col_names][2:] # 
  
  flash_msg = ""
  if request.method == 'POST':
    new_data = Project.query.get(request.form['id'])
    for column in colNames: # Type of column is string
      if column is not "id" or column is not "user_id":
        # Convert string to attribute
        setattr(new_data, column, request.form[column])
    db.session.commit()
    # flash_msg = new_data.firstname + "'s information is updated successfully"
    flash_msg = "Information updated successfully"
  flash(flash_msg)
  return redirect(url_for('myadmin.display_projects', page_num=1))

@bp.route('/delete/project/<id>/', methods=['GET', 'POST'])
def delete_project(id):
  return "hello"

@bp.route('/display/supervisors/all/<int:page_num>', methods=['GET', 'POST'])
def display_supervisors(page_num):
  col_names = Supervisor.__table__.columns
  colNames = [i.name.upper() for i in col_names] [:] # Uppercase columns' name
  attributes = [i.name for i in col_names][:] # Columns' name

  # Name of all supervisors from user table using user_id
  supervisors = Supervisor.query.all()
  superNames = []
  for supervisor in supervisors: 
    superNames.append((User.query.filter_by(id=supervisor.user_id).first()).name)

  supersFromDB = Supervisor.query.paginate(per_page=2, page=page_num, error_out=True)
  nameDic = {}
  for row in supersFromDB.items:
    nameDic[row.user_id] = User.query.filter_by(id=row.user_id).first().name 
    print(User.query.filter_by(id=row.user_id).first().name)

  # supersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('t_supervisors.html', 
                          title="Administrator", 
                          persons=supersFromDB,
                          colNames=colNames,
                          attributes=attributes,
                          superNames=superNames,
                          nameDic=nameDic)

@bp.route('/edit/supervisor/', methods=['GET', 'POST'])
def edit_supervisor():
  data = request.form
  col_names = Supervisor.__table__.columns
  # From third column to last column, excluding id and user_id
  colNames = [i.name for i in col_names][2:] #
  
  flash_msg = ""
  if request.method == 'POST':
    new_data = Supervisor.query.get(request.form['id'])
    for column in colNames: # Type of column is string
      if column is not "id" or column is not "user_id":
        # Convert string to attribute
        setattr(new_data, column, request.form[column])
    db.session.commit()
    # flash_msg = new_data.firstname + "'s information is updated successfully"
    flash_msg = "Information updated successfully"
  flash(flash_msg)
  return redirect(url_for('myadmin.display_supervisors', page_num=1))

@bp.route('/display/students/all/<int:page_num>', methods=['GET', 'POST'])
def display_students(page_num):
  col_names = Student.__table__.columns
  colNames = [i.name.upper() for i in col_names] # Capitalize columns' name
  attributes = [i.name for i in col_names] # Columns' name

  # Rearrange colNames as desired, and attributes correspondingly
  fixedCol = [7,6]
  fixedColNames = [colNames[i] for i in fixedCol]
  fixedColAttributes = [attributes[i] for i in fixedCol]
  colNamesR = colNames[2:6] + colNames[8:]
  attributesR = attributes[2:6] + attributes[8:]
  studentsFromDB = Student.query.paginate(per_page=2, page=page_num, error_out=True)
  
  # usersFromDB = user_serializer.dump(userFromDB.items)
  return render_template('t_students.html', 
                          title="Administrator", 
                          persons=studentsFromDB,
                          colNames=colNamesR,
                          attributes=attributesR,
                          fixedColNames=fixedColNames,
                          fixedColAttributes=fixedColAttributes)

@bp.route('/edit/student/', methods=['GET', 'POST'])
def edit_student():
  data = request.form
  col_names = Student.__table__.columns
  # From third column to last column, excluding id and user_id
  colNames = [i.name for i in col_names][2:] # 43 columns at the moment
  
  flash_msg = ""
  if request.method == 'POST':
    new_data = Student.query.get(request.form['id'])
    for column in colNames: # Type of column is string
      if column is not "id" or column is not "user_id":
        # Convert string to attribute
        setattr(new_data, column, request.form[column])
    db.session.commit()
    flash_msg = new_data.firstname + "'s information is updated successfully"
  flash(flash_msg)
  return redirect(url_for('myadmin.display_students', page_num=1))

@bp.route('/add/user', methods=['GET', 'POST'])
def add_user():
    data = request.form
    flash_msg = ""
    form = RegistrationForm()
    if request.method == 'POST':
        print("data: ", data)
        user = User(name=data['name'],
                    email=data['email'],
                    confirmed=False,
                    password='password', # Must send password reset email
                    registered_on=date.today(),
                    role=data['role'])
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('/auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email and reset your password"
        email.send_email(user.email, subject, html)
        flash_msg = "Email has been sent to the new user"
    flash(flash_msg)
    return redirect(url_for('myadmin.display_users', page_num=1))

@bp.route('/resolving/task/<task_id>/', methods=['GET', 'POST'])
def mark_as_resolved(task_id):
    resolve_task = AdminTask.query.get(task_id)
    resolve_task.set_task_as_resolved(True)
    resolve_task.set_task_resolved_on(datetime.datetime.now())
    db.session.add(resolve_task)
    db.session.commit()
    flash("Resolving task successfully")
    return redirect(url_for('myadmin.admin_home'))

@bp.route('/delete/<utype>/<id>/', methods=['GET', 'POST'])
def deleting(utype, id):
  del_user = ""
  if utype == "Student":
    student = Student.query.filter_by(id=id).first()
    
    del_student = Student.query.get(id)
    del_user = User.query.get(student.user_id)

    # Delete from Student table
    db.session.delete(del_student)
    # Delete from user table
    db.session.delete(del_user)
    db.session.commit()
  
  if utype == "Supervisor":
    supervisor = Supervisor.query.filter_by(id=id).first()
    
    del_supervisor = Supervisor.query.get(id)
    del_user = User.query.get(supervisor.user_id)

    # Delete from Student table
    db.session.delete(del_supervisor)
    # Delete from user table
    db.session.delete(del_user)
    db.session.commit()
  flash("Successfully deleted a user '" + del_user.email + "'")
  return redirect(url_for('myadmin.display_users', page_num=1))

