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
from thundersnow.models import Payment, User


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
