
# Import modules
from app import admin
from app import db
from app import login
from flask import redirect
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# User account class
class User(UserMixin, db.Model):
    
    # ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Username
    name = db.Column(db.String(64), index=True)
    
    # Email
    email = db.Column(db.String(128), index=True, unique=True)
    
    # Confirmed
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    
    # Password 
    password = db.Column(db.String(128))
    
    # Role (account type)
    role = db.Column(db.String(32))
    
    registered_on = db.Column(db.DateTime, nullable=False)
    
    confirmed_on = db.Column(db.DateTime, nullable=True)
    password_reset_token = db.Column(db.String, nullable=True)

    # Methods
    def set_user_password(self, new_password):
        self.password = generate_password_hash(new_password)
  
    def check_password(self, current_password):
        return check_password_hash(self.password, current_password)
  
    def set_user_role(self, new_role):
        self.role = new_role

    def set_user_name(self, new_name):
        self.name = new_name
  
    def set_user_fullname(self, new_fullname):
        self.fullname = new_fullname

    def set_user_email(self, new_email):
        self.email = new_email

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    def __init__(self, 
                name, email, password, confirmed,
                registered_on, role="", 
                confirmed_on=None,
                password_reset_token=None):

        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

        self.registered_on=registered_on
        self.role = role
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.password_reset_token = password_reset_token 


# Load user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
  

# Student information class
class Student(db.Model):
    
    # ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userId = db.relationship('User', foreign_keys=[user_id])
    
    # Fields from student details pages:
    # (Variable names match HTML names)
    
    ### Page 1
    # Title
    title = db.Column(db.String(64)) 
    
    # Gender
    gender = db.Column(db.String(64))
    
    # DOB
    dob = db.Column(db.String(64))
    
    
    ### Page 2
    # Passport name
    ppname = db.Column(db.String(128))
    
    # Surname (English) 
    surname = db.Column(db.String(128))
    
    # Surname (English)
    firstname = db.Column(db.String(128))
    
    # Preferred name
    prefname = db.Column(db.String(128))
    
    # Name in characters
    charname = db.Column(db.String(128))
    
    
    ### Page 3
    # Birth country
    birth_cntry = db.Column(db.String(128))
    
    # Citizenship country
    citizen_cntry = db.Column(db.String(128))
    
    # Street in address
    street_addr = db.Column(db.String(128))
    
    # City in address 
    city_addr = db.Column(db.String(128))
    
    # State in address 
    state_addr = db.Column(db.String(128))
    
    # Postcode in address
    postcode_addr = db.Column(db.String(128))
    
    # Country in address
    cntry_addr = db.Column(db.String(128))
    
    
    ### Page 4 
    ## Emergency contact
    
    # Name
    emg_name = db.Column(db.String(128))
    
    # Relationship
    emg_rel = db.Column(db.String(128))
    
    # Phone number
    emg_ph = db.Column(db.String(128))
    
    
    ### Page 5
    ## University Details
    uni_name = db.Column(db.String(128))
    uni_majors = db.Column(db.String(128))
    uni_gpa = db.Column(db.String(32))
    uni_years = db.Column(db.String(64))
    uni_awards = db.Column(db.String(256))
    
    
    ### Page 6
    ## English Requirements
    
    # Do they want a english program?
    eng_prog = db.Column(db.String(64))
    
    # If they want a program, which one?
    eng_prog_choice = db.Column(db.String(128))
    
    
    # Are they are a native speaker?
    native_sp = db.Column(db.String(64))
    
    
    # Additional information required from non-native speakers
    # Test name and score
    test_sc = db.Column(db.String(128))
    
    # English test file name
    eng_file = db.Column(db.String(64))
    
    ### Page 7
    ## Long Answer Questions
    longQ1 = db.Column(db.String(1600))
    longQ2 = db.Column(db.String(3100))
    longQ3 = db.Column(db.String(3100))
    longQ4 = db.Column(db.String(3100))
    
    ### Page 8
    ## File Uploads
    
    # English test file name
    cv_file = db.Column(db.String(64))
    
    # Transcript file name
    transcr_file = db.Column(db.String(64))
    
    ## Tuition
    tuition_fee = db.Column(db.String(128))
    
    # Initialize student entry
    def __init__(self, user_id):
        self.user_id = user_id


# Supervisor information class
class Supervisor(db.Model):
   
    # ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userId = db.relationship('User', foreign_keys=[user_id])
    
    # Faculty
    faculty = db.Column(db.String(128))
    
    # Faculty
    discipline = db.Column(db.String(128))
    
    # Initialize supervisor entry
    def __init__(self, user_id):
        self.user_id = user_id
        
# Project class
class Project(db.Model):
    
    # ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userId = db.relationship('User', foreign_keys=[user_id])
    
    # Project fields
    main_supervisor = db.Column(db.String(128)) 
    co_supervisor = db.Column(db.String(128)) 
    faculty = db.Column(db.String(128)) 
    school = db.Column(db.String(128)) 
    title = db.Column(db.String(128)) 
    description = db.Column(db.String(128)) 
    skills = db.Column(db.String(128)) 
    keywords = db.Column(db.String(128)) 
    email = db.Column(db.String(128), index=True, unique=True)
    campus = db.Column(db.String(128)) 
    length = db.Column(db.Integer) 
    total = db.Column(db.Integer) 
    place = db.Column(db.String(128)) 

    def __init__(self, user_id):
        self.user_id = user_id

   
# Preference class
class Preference(db.Model):
    
    # ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Project ID
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # Student ID
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


# Modifying admin model view
class MyAdminModelView(ModelView):
    # edit_template = 'edit.html'
#   pass
    @login_required
    def is_accessible(self):
        # if return is False only the Home tab is visible
        # return False
        # This is also same with return False
        if current_user.role == 'Administrator':
            return current_user.is_authenticated
        else:  
            return redirect(url_for('index'))
        
        # user + admin cannot see but others can if link is known
        # (127.0.0.1:5000/admin/user)
        return not current_user.is_authenticated
    
    # Overwriting the pre-defined function
    def inaccessible_callback(self, name, ** kwargs):
        return redirect(url_for('login'))


# Add views to admin
admin.add_view(MyAdminModelView(User, db.session))
admin.add_view(MyAdminModelView(Student, db.session))
admin.add_view(MyAdminModelView(Supervisor, db.session))
admin.add_view(MyAdminModelView(Project, db.session))
admin.add_view(MyAdminModelView(Preference, db.session))
