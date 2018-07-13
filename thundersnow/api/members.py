from flask import Blueprint, jsonify, request

from thundersnow.models import db, Member
from thundersnow.utils import login_required


members_blueprint = Blueprint('members', __name__)


@members_blueprint.route('/members')
@login_required
def members():
    members = [m.serialize for m in Member.query.order_by(Member.name).all()]
    return jsonify(members)


@members_blueprint.route('/members/<int:member_id>', methods=['GET', 'DELETE'])
@login_required
def api_member(member_id):
    """
    Get a member by id.
    """
    member = Member.query.filter_by(id=member_id).first_or_404()
    if request.method == 'GET':
        return jsonify(member.serialize)

    elif request.method == 'DELETE':
        db.session.delete(member)
        db.session.commit()
        return "Successfully deleted member", 204
