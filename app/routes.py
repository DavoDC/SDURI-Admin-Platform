
# Import modules
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

# Enable favicon support
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Main page
@app.route('/') # methods=['GET', 'POST'])
@app.route('/index') #, methods=['GET', 'POST'])
def index():
    # If user is logged in
    if current_user.is_authenticated:
        # Send to their user page
        return send_to_user_page(current_user.role);

    # Otherwise render normal
    return render_template('index.html', title='Home')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    # If user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise log in
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        # Send to correct page
        return send_to_user_page(user.role);

    # Render login page
    return render_template('auth/login.html', title='Sign In', form=form)


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():

    # If user is logged in, send back to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Otherwise register
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # Create user object
        user = User(name=form.username.data,
                    email=form.email.data)
        user.set_user_password(form.password.data)
        
        # TEMPORARY: Set role as student always
        user.set_user_role("Student")
        
        # Add user to database
        db.session.add(user)
        db.session.commit()
        
        # Notify
        flash('Congratulations, you are now a registered user!')
        
        # Send to login page
        return redirect(url_for('login'))
    
    # Show register page
    return render_template('auth/register.html', title='Register', form=form)


# Helper method: Redirect to user page
def send_to_user_page(role):
    if role == "Administrator":
        return redirect(url_for('admin', username=current_user.name))
    elif role == "Supervisor":
        return redirect(url_for('supervisors', username=current_user.name))
    elif role == "Student":
        return redirect(url_for('students', username=current_user.name))
    else:
        print("Unknown role (send_to_user_page)")


# Admin user page
@app.route('/admin/<username>')
@login_required
def admin(username):
    user = User.query.filter_by(name=username).first_or_404()
    users = User.query.all()
    return render_template('admin/admin.html', 
                           user=user, title='Admin', users=users)


# Supervisor user page
@app.route('/supervisor/<username>')
@login_required
def supervisors(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('supervisor/supervisors.html', 
                           user=user, title='Supervisor')
                           
                           
# Supervisor faculty choice page
@app.route('/supervisor-faculty')
@login_required
def supervisor_faculty():
    return render_template('supervisor/faculty.html')                       
                           
                           
# Student user page
@app.route('/student/<username>')
@login_required
def students(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('student/students.html', 
                           user=user, title='Student')

# Student details page
@app.route('/student-details')
@login_required
def student_details():
    return render_template('student/details/landing.html')


# Questions routing for student and supervisor application page series
@app.route('/student-details/pg<num>outof<max>')
#@login_required # Supervisor accounts cannot be made yet!
def question(num, max):
    # Generate path of question page
    url = 'student/details'
    url += '/pages/page'
    url += str(num) + '.html'

    # Render template with question number variables
    # - num = Question number
    # - max = Maximum question number
    return render_template(url, num=int(num), max=int(max))


# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


