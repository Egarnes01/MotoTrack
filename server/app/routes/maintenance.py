from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import MaintenanceLog
from ..utils import parse_date, get_owned_motorcycle_or_404, current_user_id

maintenance_bp = Blueprint('maintenance', __name__)


def log_to_dict(log):
    return {
        'id': log.id,
        'motorcycle_id': log.motorcycle_id,
        'service_type': log.service_type,
        'service_date': log.service_date.isoformat(),
        'mileage_at_service': log.mileage_at_service,
        'notes': log.notes,
        'cost': log.cost,
        'interval_miles': log.interval_miles,
        'interval_days': log.interval_days,
        'next_due_mileage': log.next_due_mileage(),
        'next_due_date': log.next_due_date().isoformat() if log.next_due_date() else None,
        'created_at': log.created_at.isoformat(),
    }


@maintenance_bp.get('/motorcycle/<int:motorcycle_id>')
@jwt_required()
def list_logs_for_motorcycle(motorcycle_id):
    motorcycle = get_owned_motorcycle_or_404(motorcycle_id)
    logs = MaintenanceLog.query.filter_by(motorcycle_id=motorcycle.id).order_by(MaintenanceLog.service_date.desc()).all()
    return jsonify([log_to_dict(log) for log in logs])


@maintenance_bp.post('')
@jwt_required()
def create_log():
    data = request.get_json() or {}
    required = ['motorcycle_id', 'service_type', 'service_date', 'mileage_at_service']
    missing = [field for field in required if data.get(field) in [None, '']]
    if missing:
        return jsonify({'error': f"Missing fields: {', '.join(missing)}"}), 400

    motorcycle = get_owned_motorcycle_or_404(int(data['motorcycle_id']))

    mileage_at_service = int(data['mileage_at_service'])
    if mileage_at_service > motorcycle.current_mileage:
        motorcycle.current_mileage = mileage_at_service

    log = MaintenanceLog(
        motorcycle_id=motorcycle.id,
        service_type=data['service_type'].strip(),
        service_date=parse_date(data['service_date']),
        mileage_at_service=mileage_at_service,
        notes=(data.get('notes') or '').strip() or None,
        cost=float(data['cost']) if data.get('cost') not in [None, ''] else None,
        interval_miles=int(data['interval_miles']) if data.get('interval_miles') not in [None, ''] else None,
        interval_days=int(data['interval_days']) if data.get('interval_days') not in [None, ''] else None,
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log_to_dict(log)), 201


@maintenance_bp.put('/<int:log_id>')
@jwt_required()
def update_log(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    motorcycle = get_owned_motorcycle_or_404(log.motorcycle_id)
    data = request.get_json() or {}

    if 'service_type' in data:
        log.service_type = data['service_type'].strip()
    if 'service_date' in data and data['service_date']:
        log.service_date = parse_date(data['service_date'])
    if 'mileage_at_service' in data and data['mileage_at_service'] not in [None, '']:
        log.mileage_at_service = int(data['mileage_at_service'])
    if 'notes' in data:
        log.notes = (data['notes'] or '').strip() or None
    if 'cost' in data:
        log.cost = float(data['cost']) if data['cost'] not in [None, ''] else None
    if 'interval_miles' in data:
        log.interval_miles = int(data['interval_miles']) if data['interval_miles'] not in [None, ''] else None
    if 'interval_days' in data:
        log.interval_days = int(data['interval_days']) if data['interval_days'] not in [None, ''] else None

    if log.mileage_at_service > motorcycle.current_mileage:
        motorcycle.current_mileage = log.mileage_at_service

    db.session.commit()
    return jsonify(log_to_dict(log))


@maintenance_bp.delete('/<int:log_id>')
@jwt_required()
def delete_log(log_id):
    log = MaintenanceLog.query.get_or_404(log_id)
    get_owned_motorcycle_or_404(log.motorcycle_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'message': 'Maintenance log deleted successfully.'})
