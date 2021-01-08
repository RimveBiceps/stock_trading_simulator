import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
]

bp = Blueprint('chart', __name__, url_prefix='/chart')

@bp.route('/line', methods=('GET', 'POST'))
def line():
    line_labels=labels
    line_values=values
    return render_template('charts/line.html', title='Line Chart', max=17000, labels=line_labels, values=line_values)

@bp.route('/bar', methods=('GET', 'POST'))
def bar():
    bar_labels=labels
    bar_values=values
    return render_template('charts/bar.html', title='Bar Chart', max=17000, labels=bar_labels, values=bar_values)

@bp.route('/pie', methods=('GET', 'POST'))
def pie():
    pie_labels=labels
    pie_values=values
    return render_template('charts/pie.html', title='Pie Chart', max=17000, set=zip(values, labels, colors))