from flask import Blueprint, jsonify, request

from thundersnow.models import db, Member
from thundersnow.utils import login_required


members_blueprint = Blueprint('members', __name__)


@members_blueprint.route('/members')
@login_required
def members():
    if request.args.get('with_payments'):
        members = [m.serialize_with_payments for m in Member.query.order_by(Member.name).all()] # noqa e501
    else:
        members = [m.serialize for m in Member.query.order_by(Member.name).all()] # noqa e501
    return jsonify(members)


@members_blueprint.route('/members/<int:member_id>', methods=['GET', 'DELETE', 'PUT']) # noqa e501
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
    elif request.method == 'PUT':
        if request.json.get('new_member_id'):
            member = Member.query.filter_by(id=member_id).first()

            if not member.payments:
                return 'Nothing to do', 200

            for payment in member.payments:
                setattr(payment, 'member_id', request.json['new_member_id'])
                db.session.add(payment)
                db.session.commit()

            db.session.delete(member)
            db.session.commit()
