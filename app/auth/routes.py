from app import db
from app.auth import bp
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse


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


@bp.route('/supervisor/<username>')
@login_required
def supervisors(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('supervisors.html', user=user, title='Supervisor')


@bp.route('/student/<username>')
@login_required
def students(username):
    user = User.query.filter_by(name=username).first_or_404()
    return render_template('students.html', user=user, title='Student')


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


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/register', methods=['GET', 'POST'])
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
    return redirect(url_for('auth.login'))
return render_template('register.html', title='Register', form=form)
