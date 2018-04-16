from functools import wraps
import datetime
import itertools
import os
import pylev

from flask import abort, Flask, jsonify, redirect, request, session, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

dev_config = 'thundersnow.config.DevelopmentConfig'
app_settings = os.getenv('APP_SETTINGS', dev_config)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from thundersnow.models import Member, Payment, User, Week # NOQA E402


def login_required(func):
    """
    Decorator that denotes a visitor should be logged in to
    access this endpoing.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Wrapper that checks to see if user has an active session.
        """
        if os.getenv('AUTH_DISABLED', False):
            return func(*args, **kwargs)
        elif 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))

    return wrap


def admin_required(func):
    """
    Admin required decorator functions. Also wraps login_required.
    This is used for user management and hiding incomplete featrues.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Check to see if user is an admin within the session.
        """
        admin = 'admin' in session and session['admin'] is True
        if 'logged_in' in session and admin:
            return func(*args, **kwargs)

        abort(401)
    return wrap


@app.route('/')
def index():
    """
    Main route for serving the index page.
    """
    return app.send_static_file('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """
    Log the user in.
    """
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        session['logged_in_user'] = user.id
        session['admin'] = user.admin
        return jsonify({'result': True, 'admin': user.admin})
    else:
        return jsonify({'result': False}), 404


@app.route('/api/logout')
@login_required
def logout():
    """
    Log the user out.
    """
    session.pop('logged_in', None)
    session.pop('admin', None)
    return jsonify({'result': 'success'})


@app.route('/api/status')
def status():
    """
    Check if the user is logged in and admin or not.
    """
    status = False
    admin = False
    if session.get('logged_in') and session['logged_in']:
        status = True
        if session.get('admin') and session['admin']:
            admin = True

    return jsonify({'status': status, 'admin': admin})


@app.route('/api/users', methods=['GET', 'POST'])
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


@app.route('/api/weeks', methods=['GET', 'POST'])
@login_required
def api_weeks():
    """
    Get/create week endpoint.
    """
    if request.method == 'POST':
        week_arr = request.json['week'].split('-')
        week = Week(week_arr[0], week_arr[1], week_arr[2])
        db.session.add(week)
        db.session.commit()
        return jsonify(str(week))
    else:
        year = datetime.datetime.now().year
        if request.args.get('year') and 'undefined' != request.args['year']:
            year = request.args['year']
        weeks = Week.query.filter_by(year=year).all()
        return jsonify([str(w) for w in weeks])


@app.route('/api/members')
@login_required
def api_members():
    members = [m.serialize for m in Member.query.order_by(Member.name).all()]
    return jsonify(members)


@app.route('/api/members/<int:id>')
@login_required
def api_member(id):
    member = Member.query.filter_by(id=id).first_or_404()
    return jsonify(member.serialize)


@app.route('/api/members/<int:id>/payments')
@login_required
def api_member_payments(id):
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


@app.route('/api/reports/annual/<int:year>')
@login_required
def api_annual_reports(year):
    """
    Produce the annual payment report. given a year.
    """
    pmts = Payment.query.join(Week).filter(Week.year == year).all()

    grouped = {}
    for p in pmts:
        serialized = p.serialize
        name = grouped.get(serialized['name'])
        if name:
            mapped_pmts = grouped.get(serialized['name'])
            serialized.pop('name')
            mapped_pmts.append(serialized)
        else:
            name = serialized.pop('name')
            grouped[name] = [serialized]
            # grouped[name]['sum']
    to_return = []
    for k, v in grouped.items():
        total = 0
        # this is horrid variabble naming, have you no shame?!
        for x in v:
            total += x.get('amount')

        to_return.append({'name': k, 'payments': v, 'total': total})

    return jsonify(to_return)


@app.route('/api/names/similar')
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


@app.route('/api/payment', methods=['GET', 'POST'])
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
                month=month,
                day=day,
                year=year
            ).first()
            pmts = Payment.query.filter_by(week=week).all()
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


@app.route('/api/payment/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_payment(payment_id):
    """
    Get a payment by it's id.
    """
    payment = Payment.query.filter_by(id=payment_id).first_or_404()

    if request.method == 'PUT':
        # TODO: lookup date as well, how do we change that?
        setattr(payment, 'check_number', request.json.get('checkNumber'))
        setattr(payment, 'amount', request.json.get('amount'))
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.serialize)

    elif request.method == 'DELETE':
        db.session.delete(payment)
        db.session.commit()
        return "Successfully deleted payment", 204


def split_json_date(date_str):
    """
    Turn a date string formatted like mm-dd-YYYY into a datetime.date obj.
    """
    date_array = date_str.split('-')
    month = int(date_array[0])
    day = int(date_array[1])
    year = int(date_array[2])
    return month, day, year
