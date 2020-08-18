from flask import redirect, url_for
from app import app, db, login, admin
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView




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

@login.user_loader
def load_user(id):
  return User.query.get(int(id))
  

class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(128)) # Drop down list
  name = db.Column(db.String(64), index=True) # Name (as it appears in your passport):
  surname = db.Column(db.String(64), index=True) # Surname (in English):
  # more lines to be added
  #
  #

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  userId = db.relationship('User', foreign_keys=[user_id])


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
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
        
    
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