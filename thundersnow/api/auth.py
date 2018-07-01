from flask import Blueprint, jsonify, request, session

from thundersnow import bcrypt
from thundersnow.models import User
from thundersnow.utils import login_required


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Log the user in.
    """
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        session['logged_in_user'] = user.id
        session['admin'] = user.admin
        return jsonify({'result': True, 'admin': user.admin})
    else:
        return jsonify({'result': False}), 404


@auth_blueprint.route('/logout')
@login_required
def logout():
    """
    Log the user out.
    """
    session.pop('logged_in', None)
    session.pop('admin', None)
    return jsonify({'result': 'success'})


@auth_blueprint.route('/status')
def status():
    """
    Check if the user is logged in and admin or not.
    """
    status = False
    admin = False
    if session.get('logged_in') and session['logged_in']:
        status = True
        if session.get('admin') and session['admin']:
            admin = True

    return jsonify({'status': status, 'admin': admin})
