from datetime import date, datetime
from flask_jwt_extended import get_jwt_identity
from flask import abort
from .models import User, Motorcycle


def parse_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(value, '%Y-%m-%d').date()


def current_user_id():
    identity = get_jwt_identity()
    return int(identity)


def get_owned_motorcycle_or_404(motorcycle_id):
    motorcycle = Motorcycle.query.get_or_404(motorcycle_id)
    if motorcycle.user_id != current_user_id():
        abort(403, description='You do not have access to this motorcycle.')
    return motorcycle
