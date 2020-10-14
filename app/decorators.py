from flask import flash
from flask import redirect
from flask import url_for
from flask_login import current_user
from functools import wraps

# This function can be used for anywhere
# email confirmation is a prerequisite action
def check_confirmed(function):
    @wraps(function)
    def decorated_function(*args, ** kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return function(*args, ** kwargs)

return decorated_function