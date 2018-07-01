from flask import Blueprint, jsonify, request

from thundersnow import db
from thundersnow.models import User
from thundersnow.utils import admin_required

users_blueprint = Blueprint('user', __name__)


@users_blueprint.route('/api/users', methods=['GET', 'POST'])
@admin_required
def api_users():
    """
    Get/Create User's endpoint.
    """
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        # set admin to False incase this ever ends up in register flow
        user = User(email=email, password=password, admin=False)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize)
    else:
        return jsonify([u.serialize for u in User.query.all()])
