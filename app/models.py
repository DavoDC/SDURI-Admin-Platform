
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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True) # Preferred Name
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10))


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

# Load user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
  

# Student class
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Title
    title = db.Column(db.String(64)) 
    
    # Gender
    gender = db.Column(db.String(64))
    
    # DOB
    dob = db.Column(db.String(64))
    
    # English test file name
    eng_file = db.Column(db.String(64))
       
#    name = db.Column(db.String(64), index=True) # Name (as it appears in your passport):
#    surname = db.Column(db.String(64), index=True) # Surname (in English):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userId = db.relationship('User', foreign_keys=[user_id])
    
    def __init__(self, user_id, title, name, surname):
        self.user_id = user_id
        self.title = title
        self.name = name
        self.surname = surname


# Project class
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    userId = db.relationship('User', foreign_keys=[user_id])

# Preference class
class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


# # Customized admin interface
# class CustomView(ModelView):
#     list_template = 'list.html'
#     create_template = 'create.html'
#     edit_template = 'edit.html'


# class UserAdmin(CustomView):
#     column_searchable_list = ('name',)
#     column_filters = ('name', 'email')

# # Add views
# # admin.add_view(UserAdmin(User, db.session))
# # admin.add_view(CustomView(Page, db.session))
# admin = Admin(app, name='Home', template_mode='bootstrap3')

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
        
        # user + admin cannot see but others can if link is known(127.0.0.1:5000/admin/user)
        return not current_user.is_authenticated
    
    # Overwriting the pre-defined function
    def inaccessible_callback(self, name, ** kwargs):
        return redirect(url_for('login'))
        

# Add views to admin
admin.add_view(MyAdminModelView(User, db.session))
admin.add_view(MyAdminModelView(Student, db.session))
admin.add_view(MyAdminModelView(Project, db.session))
admin.add_view(MyAdminModelView(Preference, db.session))


# # admin.add_view(MyAdminModelView(QuizzMarks, db.session))
# admin.add_view(MyAdminModelView(Role, db.session))
# admin.add_view(MyAdminModelView(Quiz, db.session))
# admin.add_view(MyAdminModelView(quizQuestions, db.session))
# admin.add_view(MyAdminModelView(quizAnswers, db.session))
# admin.add_view(MyAdminModelView(quizAttempt, db.session))
# admin.add_view(MyAdminModelView(quizOptions, db.session))

# admin.add_view(UserView(User, db.session, category="Team"))