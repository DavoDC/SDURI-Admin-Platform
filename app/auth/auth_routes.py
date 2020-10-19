from app import db
from app import email
from app import mail
from app import routes
from app.auth import bp
from app.auth.auth_forms import *
from app.auth.token import *
from app.models import *
from app.myadmin.myadmin_models import *
import datetime
from datetime import date
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_mail import Message


# Initial registratioon
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
        
        # Try to send email
        try:
            mail.send(msg)
        except Exception as e:
            err_msg = "There was an error when sending the email."
            err_msg += ". An internet issue, VPN or"
            err_msg += "firewall may be interfering."
            flash(err_msg)
            return redirect(url_for('index'))
        
 
        flash("Please click the confirmation link sent to your email to continue the registration process.", "warning")
  
        # url_for in above cases do not show back the provided email so render_template is used as below
        render_template('/auth/initial_registration.html', form=initialForm, roles=roles)
  
    return render_template('/auth/initial_registration.html', form=initialForm, roles=roles)



# Continuing registration process
@bp.route('/initial-pwd-setting/<token>', methods=['GET', 'POST'])
def initial_pwd_setting(token):
    """Confirm email and set password for the first time"""
    roles = ["Student", "Supervisor"]
    form = InitialPasswordNameForm()
    # Get email from the token
    email_fr_token = confirm_token(token)
    # user = User.query.filter_by(email=current_user.email).first_or_404()
    user = User.query.filter_by(email=email_fr_token).first_or_404()
    # if user.email == email_fr_token:

    flash_msg = "" # flash message
    flash_msg_cat = "" # flash message category
    # If a supervisor uses email that does not contain
    # "@uwa.edu.au" confirmation is required from administrator
    confirmed_required = False
    if form.validate_on_submit():
        if user: # Double checking user object from above
            # By default, user.role is "Student" except for
            # users' email that contains "@uwa.edu.au"
            # This condition checks if someone wants to be
            # a supervisor but not using an email that
            # does not contain "@uwa.edu.au"
            if user.role != form.role.data and \
                form.role.data == "Supervisor":
                # Request confirmation from administrator
                confirmed_required = True
                flash_msg = 'Action required: Administrator confirmation'
                flash_msg_cat = 'warning'
                # Change this code below
                # Send notification to admin email or
                # task list on home page

                t_description = "Check users who are waiting for your confirmation"
                t_action = "Confirm user's role"
                task = AdminTask(description=t_description,
                                 action=t_action,
                                 userEmail=email_fr_token)
                db.session.add(task)
                db.session.commit()

            else:
                user.confirmed = True
                user.confirmed_on = datetime.datetime.now()
                flash_msg = 'Account creation successfully completed.'
                flash_msg_cat = 'success'

        user.set_user_name(form.name.data)
        user.set_user_password(form.password.data)
        user.password_reset_token = None
        db.session.commit()



        flash(flash_msg, flash_msg_cat)
        return render_template('index.html')

    # Need to get password and name, otherwise cannot go to user home page
    # after clicking the login button on login page because
    # username is required as shown in this function [def students(username):]
    return render_template('/auth/initial_pwd_name.html', form=form, roles=roles)


@bp.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordReset(request.form)
    pwChangeForm = ChangePasswordForm(request.form)
    if form.validate_on_submit():

        # Get user
        user = User.query.filter_by(email=form.email.data).first()

        # Get token and save
        token = generate_confirmation_token(user.email)
        user.password_reset_token = token
        db.session.commit()

        # Get messsage
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        html = render_template('auth/pwreset_msg.html',
                               username=user.email,
                               reset_url=reset_url)
        subject = ""
        msg = Message(subject,
                      recipients=[user.email],
                      sender="no-reply@gmail.com")
        msg.html = html

        # Send message
        mail.send(msg)



        #email.send_email(user.email, subject, html)

        flash('A password reset email has been sent via email.', 'success')
        return redirect(url_for("index"))
    return render_template('forgot_password.html', form=form)



@bp.route('/password/forgot/new/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ChangePasswordForm(request.form)
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()

    if user.password_reset_token is not None:

        if form.validate_on_submit():

            user = User.query.filter_by(email=email).first()
            if user != None:
                user.password = generate_password_hash(form.password.data)
                user.password_reset_token = None
                db.session.commit()

                flash('Password successfully changed.', 'success')
                return redirect(url_for('index'))

            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('index'))

        else:
            flash('Cannot reset password, try again.', 'danger')
    else:
        flash('This reset link has expired.', 'danger')
        return 'This reset link has expired.'

    return render_template('reset_password.html', form=form)


@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('students', username=current_user.name)) # need to change depending on user
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    # return redirect(url_for('main.students')) # return for other user types
    return redirect(url_for('index'))



@bp.route('/unconfirmed', methods=['GET', 'POST'])
def unconfirmed():
    return render_template('unconfirmed.html')



@bp.route('/resend')
@login_required
def resend_confirmation():
    # email = request.args.get('unconfirmed_email')

    # token = generate_confirmation_token(use.email)
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('/auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    # this user.email may to be changed to current_user.email
    # email.send_email(user.email, subject, html)
    email.send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))


