import itertools

from flask import Blueprint, jsonify, request
import pylev

from thundersnow.models import Member, Payment, Week
from thundersnow.utils import admin_required, login_required


members_blueprint = Blueprint('members', __name__)


@members_blueprint.route('/members')
@login_required
def members():
    members = [m.serialize for m in Member.query.order_by(Member.name).all()]
    return jsonify(members)


@members_blueprint.route('/members/<int:id>')
@login_required
def member(id):
    member = Member.query.filter_by(id=id).first_or_404()
    return jsonify(member.serialize)


@members_blueprint.route('/members/<int:id>/payments')
@login_required
def member_payments(id):
    q = Member.id == id
    if request.args.get('year') and request.args['year'] != 'undefined':
        pmts = Payment.query \
            .join(Week).filter(Week.year == request.args['year']) \
            .join(Member).filter(Member.id == id).all()
        if len(pmts) < 1:
            return jsonify([])
    else:
        pmts = Payment.query.join(Member).join(Week).filter(q).all()
    return jsonify([p.serialize for p in pmts])


@members_blueprint.route('/members/similar')
@login_required
@admin_required
def find_similar_names():
    """
    Find members with similar names. This is used to fix
    near duplicates like Last, First vs Last,First
    """
    names = [str(m) for m in Member.query.all()]
    similar_names = {}
    for left, right in itertools.combinations(names, 2):
        distance = pylev.levenshtein(left, right)
        if distance < 3:
            similar_names['a'].append(left)
            similar_names['b'].append(right)

    return jsonify(similar_names)
