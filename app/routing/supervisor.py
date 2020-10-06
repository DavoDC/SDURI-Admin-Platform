
# Import modules
from app import app
from app import utils
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
    baseURL = url_for('supervisor_add', username=current_user.name)
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


