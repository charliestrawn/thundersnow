from functools import wraps
import os

from flask import abort, redirect, session, url_for


def login_required(func):
    """
    Decorator that denotes a visitor should be logged in to
    access this endpoing.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Wrapper that checks to see if user has an active session.
        """
        if os.getenv('AUTH_DISABLED', False):
            return func(*args, **kwargs)
        elif 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))

    return wrap


def admin_required(func):
    """
    Admin required decorator functions. Also wraps login_required.
    This is used for user management and hiding incomplete featrues.
    """
    @login_required
    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Check to see if user is an admin within the session.
        """
        if 'admin' in session and session['admin'] is True:
            return func(*args, **kwargs)
        abort(401)
    return wrap


def split_json_date(date_str):
    """
    Turn a date string formatted like mm-dd-YYYY into a datetime.date obj.
    """
    date_array = date_str.split('-')
    month = int(date_array[0])
    day = int(date_array[1])
    year = int(date_array[2])
    return month, day, year
