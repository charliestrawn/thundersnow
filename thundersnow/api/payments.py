import json
import time

import boto3
from flask import Blueprint, jsonify, request, session

from thundersnow.models import db, Member, Payment, Week
from thundersnow.utils import login_required, split_json_date

payments_blueprint = Blueprint('payment', __name__)


@payments_blueprint.route('/payment', methods=['GET', 'POST'])
@login_required
def api_payments():
    """
    Get/Create payment endpoint.
    """
    if request.method == 'GET':
        if request.args.get('year') and request.args['year'] != 'undefined':
            q = Week.year == request.args['year']
            pmts = Payment.query.join(Week).filter(q).all()
            return jsonify([p.serialize for p in pmts])

        elif request.args.get('week') and request.args['week'] != 'undefined':
            month, day, year = split_json_date(request.args['week'])
            week = Week.query.filter_by(
                month=month, day=day, year=year
            ).first()
            pmts = Payment.query.filter_by(week=week).all()
            return jsonify([p.serialize for p in pmts])
        elif request.args.get('member_id'):
            pmts = Payment.query.filter_by(member_id=request.args['member_id'])
            return jsonify([p.serialize for p in pmts])

        return jsonify([])

    elif request.method == 'POST':
        month, day, year = split_json_date(request.json.get('date'))
        week = Week.query.filter_by(month=month, day=day, year=year).first()
        if not week:
            week = Week(month=month, day=day, year=year)

        name = request.json.get('name')
        member = Member.query.filter_by(name=name).first()
        if not member:
            member = Member(request.json.get('name'))

        # Legacy support
        check_number = request.json.get('checkNumber')
        if not check_number:
            check_number = request.json.get('check_number')

        # Convert to cents
        amount = float(request.json.get('amount')) * 100
        payment = Payment(
            check_number=check_number,
            amount=amount,
            entered_by=session['logged_in_user']
        )

        week.payments.append(payment)
        member.payments.append(payment)

        db.session.add(week)
        db.session.add(member)
        db.session.add(payment)
        db.session.commit()

        return jsonify(payment.serialize), 201


@payments_blueprint.route('/payment/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_payment(payment_id):
    """

    """
    payment = Payment.query.filter_by(id=payment_id).first_or_404()

    if request.method == 'PUT':
        # TODO: lookup date as well, how do we change that?
        if request.json.get('checkNumber'):
            setattr(payment, 'check_number', request.json['checkNumber'])
        if request.json.get('amount'):
            setattr(payment, 'amount', request.json['amount'])
        if request.json.get('member_id'):
            setattr(payment, 'member_id', request.json['member_id'])
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.serialize)

    elif request.method == 'DELETE':
        db.session.delete(payment)
        db.session.commit()
        return "Successfully deleted payment", 204


@payments_blueprint.route('/backup', methods=['POST'])
@login_required
def backup():
    payments = Payment.query.join(Week).filter(Week.year == 2018).all()
    pmts = [p.serialize for p in payments]
    date = time.strftime("%m-%d-%Y")
    s3 = boto3.resource('s3')
    file_name = f'test-offering-backup-{date}'
    s3_obj = s3.Object('thundersnow-v2-bak', file_name)
    resp = s3_obj.put(Body=json.dumps(pmts))
    print(resp)
    return f'Successfully uploaded {file_name}', 200
