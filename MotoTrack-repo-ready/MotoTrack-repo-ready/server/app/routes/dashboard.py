from datetime import date
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ..models import Motorcycle, MaintenanceLog
from ..utils import current_user_id

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.get('')
@jwt_required()
def get_dashboard():
    motorcycles = Motorcycle.query.filter_by(user_id=current_user_id()).all()
    today = date.today()
    dashboard_items = []

    for motorcycle in motorcycles:
        logs = MaintenanceLog.query.filter_by(motorcycle_id=motorcycle.id).order_by(MaintenanceLog.service_date.desc()).all()
        due_services = []
        recent_logs = []

        for log in logs:
            next_due_mileage = log.next_due_mileage()
            next_due_date = log.next_due_date()
            due_by_mileage = next_due_mileage is not None and motorcycle.current_mileage >= next_due_mileage
            due_by_date = next_due_date is not None and today >= next_due_date

            if due_by_mileage or due_by_date:
                due_services.append({
                    'service_type': log.service_type,
                    'last_service_date': log.service_date.isoformat(),
                    'last_service_mileage': log.mileage_at_service,
                    'next_due_mileage': next_due_mileage,
                    'next_due_date': next_due_date.isoformat() if next_due_date else None,
                    'status': 'Due now',
                })

            recent_logs.append({
                'id': log.id,
                'service_type': log.service_type,
                'service_date': log.service_date.isoformat(),
                'mileage_at_service': log.mileage_at_service,
            })

        dashboard_items.append({
            'motorcycle': {
                'id': motorcycle.id,
                'nickname': motorcycle.nickname,
                'make': motorcycle.make,
                'model': motorcycle.model,
                'year': motorcycle.year,
                'current_mileage': motorcycle.current_mileage,
            },
            'due_services': due_services,
            'recent_logs': recent_logs[:5],
            'total_logs': len(recent_logs),
        })

    return jsonify(dashboard_items)
