from functools import wraps

from flask import redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            #flash("You need to be an admin to view this page.")
            return redirect('/')

    return wrap

def moderator_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "moderator" or current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            #flash("You need to be an admin or moderator to view this page.")
            return redirect('/')

    return wrap
