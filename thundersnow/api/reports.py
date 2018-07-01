from flask import Blueprint, jsonify

from thundersnow.models import Payment, Week
from thundersnow.utils import login_required

reports_blueprint = Blueprint('report', __name__)


@reports_blueprint.route('/reports/annual/<int:year>')
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
