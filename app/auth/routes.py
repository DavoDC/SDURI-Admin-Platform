
#from flask import request
from app import db
from app import email
from app import mail
from app.auth import bp
from app.auth.auth_forms import *
from app.auth.auth_forms import InitialRegistrationForm
from app.auth.token import *
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import *
from app.models import User
from datetime import date
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_mail import Message

# @bp.route('/')  # methods=['GET', 'POST'])
# @bp.route('/index')  # , methods=['GET', 'POST'])
# # @login_required
# def index():
#   return render_template('auth/index.html', title='Home')


@bp.route('/admin/<username>')
@login_required
def admin(username):
    user = User.query.filter_by(name=username).first_or_404()
    users = User.query.all()
    return render_template('auth/admin.html', user=user, title='Admin', users=users)





@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))

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
    return render_template('auth/login.html', title='Sign In', form=form)






@bp.route('/initial-registration', methods=['GET', 'POST'])
def initial_registration():
    initialForm = InitialRegistrationForm()
    roles = ["Student", "Supervisor"]
    if initialForm.validate_on_submit():
    
        newUser = User(name="",
                       email=initialForm.email.data,
                       password="",
                       confirmed=False,
                       registered_on=date.today(),
                       #  role=initialForm.role.data)
                       role="")
    
    
        # If email contains "@uwa.edu.au"
        if "@uwa.edu.au" in newUser.email:
            # Set user role to "Supervisor"
            newUser.set_user_role("Supervisor")
        elif "@student.uwa.edu.au" in newUser.email:
            # Else If email contains "@student.uwa.edu.au"
            # Set user role to "Student"
            newUser.set_user_role("Student")
        elif "@admin.com" in newUser.email:
            # Else If email contains "@admin"
            # Set user role to "Administrator"
            newUser.set_user_role("Administrator")
        else:
            # Else for all other emails
            # Give Student role by default
            newUser.set_user_role("Student")

        token = generate_confirmation_token(newUser.email)
    
        newUser.password_reset_token = token


        db.session.add(newUser)
        db.session.commit()

        _url = url_for('auth.initial_pwd_setting', token=token, _external=True)
        html = render_template('auth/initial_ac_confirmation_msg.html',
                               confirmation_url=_url)
        subject = "Initial Account Confirmation"
        msg = Message(subject,
                      recipients=[newUser.email],
                      sender="no-reply@gmail.com")
        msg.html = html
        mail.send(msg)
        # email.send_email(newUser.email, subject, "hello")
        
        flash("Please click the confirmation link sent to the email given below to continue registration processes.", "warning")
        # return redirect(url_for('auth.initial_registration', form=initialForm, roles=roles )) 
        # return redirect(url_for('auth.initial_registration')) 
        # url_for in above cases do not show back the provided email so render_template is used as below
        render_template('/auth/initial_registration.html', form=initialForm, roles=roles)
  
    return render_template('/auth/initial_registration.html', form=initialForm, roles=roles)

