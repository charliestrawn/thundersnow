"""
models contains the SQLAlchemy mappings for our data. Consider
breaking this out into seperate files in a models module.
- User
- Member
- Payment
- Week
- BlacklistToken
"""
from datetime import datetime, timedelta
import jwt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from thundersnow import app, db, bcrypt


class User(db.Model):
    """
    Represents a User of the application.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registered_on = datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'admin': self.admin,
            'registered_on': self.registered_on
        }


class Member(db.Model):
    """
    Members make the payments.
    """
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    payments = relationship('Payment', backref='member')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Payment(db.Model):
    """
    Payments are for a given week. They have a dollar amount and
    an optional check number.
    """
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    check_number = db.Column(db.String(50))
    amount = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.Integer, ForeignKey('members.id'))
    week_id = db.Column(db.Integer, ForeignKey('weeks.id'))
    entered_by = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, check_number, amount, entered_by):
        self.check_number = check_number
        self.amount = amount
        self.entered_by = entered_by

    def __repr__(self):
        return '<Payment {} {} {} {}'.format(self.week, self.check_number,
                                             self.amount, self.member.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date': str(self.week),
            'checkNumber': self.check_number,
            'amount': float(self.amount / 100),
            'name': self.member.name,
            'entered_by': self.entered_by
        }


class Week(db.Model):
    """
    Week represents a day technically. Payments have only been made
    on a weekly basis thus far. This allows us to aggregate payments
    for a given week.
    """
    __tablename__ = "weeks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    payments = relationship("Payment", backref="week")

    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

    def __repr__(self):
        return '{m}-{d}-{y}'.format(m=self.month, d=self.day, y=self.year)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'month': self.month,
            'day': self.day,
            'year': self.year
        }

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
