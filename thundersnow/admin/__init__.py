import itertools
import json
import os

from flask import (
    Blueprint, redirect, render_template,
    render_template_string, request, url_for
)
import pylev
import requests
from sqlalchemy.sql import func

from thundersnow.models import db, Member, Payment, Week
from thundersnow.utils import admin_required, split_json_date


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/restore', methods=['GET', 'POST'])
@admin_required
def restore_data_from_backup():
    """
    Produce the annual payment report. given a year.
    """
    if request.method == 'POST':
        payments = json.load(request.files['file'])
        for payment in payments:
            # May have to catch something here if dates aren't formatted right
            month, day, year = split_json_date(payment.get('date'))

            week = Week.query.filter_by(
                month=month, day=day, year=year
            ).first()
            if not week:
                week = Week(month=month, day=day, year=year)

            name = payment.get('name')
            member = Member.query.filter_by(name=name).first()
            if not member:
                member = Member(payment.get('name'))

            check_number = payment.get('checkNumber')
            if not check_number:
                check_number = payment.get('check_number')

            # Convert to cents
            amount = payment.get('amount') * 100
            payment = Payment(
                check_number=check_number, amount=amount, entered_by=1
            )
            week.payments.append(payment)
            member.payments.append(payment)

            db.session.add(week)
            db.session.add(member)
            db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('restore.html')


@admin_blueprint.route('/stats')
@admin_required
def stats():
    qry = db.session.query(
        func.sum(Payment.amount)
    )
    amount = qry.first()[0] / 100
    return render_template_string("Total: ${{amount}}", amount=amount)


@admin_blueprint.route('/export')
@admin_required
def get_export():
    breeze_url = os.getenv('BREEZE_API_URL')
    breeze_api_key = os.getenv('BREEZE_API_KEY')
    headers = {'Api-Key': breeze_api_key, 'Content-Type': 'application/json'}
    resp = requests.get(f'{breeze_url}/people', headers=headers)
    json_resp = resp.json()
    members = Member.query.order_by(Member.name).all()

    data = {}
    match_ids = []
    for m in members:
        # if we've already saved the ID, no need to export
        if m.breeze_id:
            continue

        data[m.id] = {'name': m.name, 'payments': len(m.payments)}
        for mem in json_resp:
            breeze_name = f'{mem["last_name"]}, {mem["first_name"]}'
            if breeze_name in m.name and m.id not in match_ids:
                match_ids.append(m.id)
                data[m.id].update({
                    'breeze_last_name': mem['last_name'],
                    'breeze_first_name': mem['first_name'],
                    'breeze_id': mem['id'],
                    'exact_match': breeze_name == m.name
                })

    return render_template('export.html', members=data)


@admin_blueprint.route('/save-breeze-id', methods=['POST'])
@admin_required
def save_breeze_id():
    member_id = request.json['member_id']
    member = Member.query.filter_by(id=member_id).first()
    setattr(member, 'breeze_id', request.json['breeze_id'])
    db.session.add(member)
    db.session.commit()

    return f'Updated member.', 200


@admin_blueprint.route('/similar-members')
@admin_required
def get_similar_members():
    members = Member.query.all()
    similar_members = {'a': [], 'b': []}
    for left, right in itertools.combinations(members, 2):
        distance = pylev.levenshtein(left.name, right.name)
        if distance < 4:
            left_json = left.serialize
            left_json['pmts'] = len(left.payments)
            similar_members['a'].append(left_json)
            right_json = right.serialize
            right_json['pmts'] = len(right.payments)
            similar_members['b'].append(right_json)

    return render_template(
        'similar.html',
        similar_members=similar_members,
        count=len(similar_members['a'])
    )


@admin_blueprint.route('/fix-similar', methods=['POST'])
@admin_required
def fix_similar_members():
    old_id = request.json['old_member_id']
    payments = Payment.query.filter_by(member_id=old_id).all()
    member = Member.query.filter_by(id=old_id).first()

    if not payments or not member:
        return 'Nothing to do', 200

    removed = len(payments)
    for payment in payments:
        setattr(payment, 'member_id', request.json['new_member_id'])
        db.session.add(payment)
        db.session.commit()

    db.session.delete(member)
    db.session.commit()

    return f'Updated {removed} payments.', 200
