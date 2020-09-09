
# Import modules
from app import app
from app.forms import LoginForm
from app.models import User
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user


# Main page
@app.route('/') # methods=['GET', 'POST'])
@app.route('/index') #, methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html', title='Home')

# Enable favicon support
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Admin user page
@app.route('/admin/<username>')
@login_required
def admin(username):
    user = User.query.filter_by(name=username).first_or_404()
    users = User.query.all()
    return render_template('admin.html', user=user, title='Admin', users=users)

# Supervisor user page
@app.route('/supervisor/<username>')
@login_required
def supervisors(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('supervisors.html', user=user, title='Supervisor')

# Supervisor application page
# TO BE RE-ROUTED BEHIND LOGIN
@app.route('/supervisor-application')
def supervisor_appl():
    return render_template('application/supervisor/landing.html')

# Student user page
@app.route('/student/<username>')
@login_required
def students(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('students.html', user=user, title='Student')

# Student application page
# TO BE RE-ROUTED BEHIND LOGIN
@app.route('/student-application')
def student_appl():
    return render_template('application/student/landing.html')

# Questions routing for student and supervisor application page series
@app.route('/<user_type>-application/question<num>outof<max>')
def question(user_type, num, max):
    # Generate URL of question page
    url = 'application/' + user_type
    url += '/question' + str(num) + '.html'

    # Render template with question number variables
    # - num = Question number
    # - max = Maximum question number
    return render_template(url, num=int(num), max=int(max))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #   next_page = url_for('index')
        # return redirect(next_page)
        # return redirect(url_for('index.html')) # Use if next_page or next variable is not used
        if user.role == "Administrator":
            return redirect(url_for('admin', username=current_user.name))
        elif user.role == "Supervisor":
            return redirect(url_for('supervisors', username=current_user.name))
        else:
            return redirect(url_for('students', username=current_user.name))
    return render_template('login.html', title='Sign In', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(name=form.username.data,  
                # user_fullname=form.user_fullname.data,
                email=form.email.data)
    user.set_user_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/project_list')
def project_list():
  #user = User.query.filter_by(name=username).first_or_404()
  return render_template('project-list.html', title='Project list')

#@app.route('/single_project', defaults={'username': None})
@app.route('/single_project')
def single_project():
  if current_user.is_authenticated:
    return render_template('single_project.html', title='Project specifics', logged=True)
  else:
  #user = User.query.filter_by(name=username).first_or_404()
    return render_template('single_project.html', title='Project specifics', logged=False)

