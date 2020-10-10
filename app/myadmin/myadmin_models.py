from app import admin
from app import db
from app import login
from app.models import *
import datetime
from flask import redirect
from flask import render_template
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class AdminTask(db.Model):
    __tablename__ = 'admin_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    action = db.Column(db.String)
    # Email cannot be unique because same user may have one or more problems
    relatedUserEmail = db.Column(db.String(120)) 
    resolved = db.Column(db.Boolean, default=False, nullable=False)
    resolved_on = db.Column(db.DateTime) # , nullable=False)

    def set_task_as_resolved(self, task_status):
        self.resolved = task_status

    def set_task_resolved_on(self, task_resolved_date):
        self.resolved_on = task_resolved_date

    def __init__(self, description, action, userEmail):
        self.description = description
        self.action = action
        self.relatedUserEmail = userEmail

    def __repr__(self):
        return '<AdminTasks {}>'.format(self.description)

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


admin.add_view(MyAdminModelView(AdminTask, db.session))
