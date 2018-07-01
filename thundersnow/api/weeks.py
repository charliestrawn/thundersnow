import datetime

from flask import Blueprint, jsonify, request

from thundersnow import db
from thundersnow.utils import login_required
from thundersnow.models import Week


weeks_blueprint = Blueprint('weeks', __name__)


@weeks_blueprint.route('/weeks', methods=['GET', 'POST'])
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
