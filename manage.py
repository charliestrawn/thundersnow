"""
manage.py conatins helper functions for bootstrapping and migrating the
payment tracker data.
"""
import json
import os
import time
import unittest

from flask_script import Manager
from thundersnow import app, db
from thundersnow.models import Member, Payment, User, Week
from thundersnow.utils import split_json_date


MANAGER = Manager(app)


@MANAGER.command
def create_admin():
    """
    Creates an admin user and normal user from the envvars
    ADMIN_EMAIL ADMIN_PASSWORD and USER_EMAIL USER_PASSWORD.

    The Admin flag was originally created to hide new features.
    """
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    if admin_email and admin_password:
        admin_user = User(
            email=admin_email, password=admin_password, admin=True
        )
        db.session.add(admin_user)

    user_email = os.getenv('USER_EMAIL')
    user_password = os.getenv('USER_PASSWORD')
    if user_email and user_password:
        user = User(
            email=user_email, password=user_password
        )
        db.session.add(user)

    db.session.commit()


@MANAGER.command
@MANAGER.option('-f', '--file', help='file to backup data to.')
def backup_data(file_name=None):
    """
    Backup the database to a json file, optionally providing a
    filename.
    """
    payments = Payment.query.all()
    date = time.strftime("%m-%d-%Y")
    if not file_name:
        name = '/home/ubuntu/backup_data/payments-backup-{}.json'
        file_name = name.format(date)
    with open(file_name, 'w') as out_file:
        payments_json = [p.serialize for p in payments]
        out_file.write(json.dumps(payments_json))

    # Printing the filename lets us store it as a variable to pass into s3 cp
    print(file_name)


@MANAGER.command
@MANAGER.option('-f', '--file', help='file to read data in from')
def restore(file_name='backup.json'):
    with open(file_name) as f:
        payments = json.load(f)
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
            print('Added payment.')


@MANAGER.command
def test():
    """
    Runs the unit tests without test coverage.
    """
    tests = unittest.TestLoader().discover(
        'thundersnow/tests', pattern='test*.py'
    )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    MANAGER.run()
