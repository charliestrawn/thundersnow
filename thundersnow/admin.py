import json

from flask import (
    Blueprint, redirect, render_template_string, request, url_for
)
from sqlalchemy.sql import func

from thundersnow import db
from thundersnow.models import Member, Payment, Week
from thundersnow.utils import admin_required, split_json_date


admin_blueprint = Blueprint('admin', __name__)


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
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@admin_blueprint.route('/stats')
def stats():
    qry = db.session.query(
        func.sum(Payment.amount)
    )
    amount = qry.first()[0] / 100
    return render_template_string("Total: ${{amount}}", amount=amount)
