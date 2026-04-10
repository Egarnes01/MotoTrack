from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import Motorcycle
from ..utils import current_user_id, get_owned_motorcycle_or_404

motorcycles_bp = Blueprint('motorcycles', __name__)


def motorcycle_to_dict(m):
    return {
        'id': m.id,
        'nickname': m.nickname,
        'make': m.make,
        'model': m.model,
        'year': m.year,
        'current_mileage': m.current_mileage,
        'vin': m.vin,
        'notes': m.notes,
        'created_at': m.created_at.isoformat(),
    }


@motorcycles_bp.get('')
@jwt_required()
def list_motorcycles():
    motorcycles = Motorcycle.query.filter_by(user_id=current_user_id()).order_by(Motorcycle.created_at.desc()).all()
    return jsonify([motorcycle_to_dict(m) for m in motorcycles])


@motorcycles_bp.post('')
@jwt_required()
def create_motorcycle():
    data = request.get_json() or {}
    required = ['nickname', 'make', 'model', 'year', 'current_mileage']
    missing = [field for field in required if data.get(field) in [None, '']]
    if missing:
        return jsonify({'error': f"Missing fields: {', '.join(missing)}"}), 400

    motorcycle = Motorcycle(
        user_id=current_user_id(),
        nickname=data['nickname'].strip(),
        make=data['make'].strip(),
        model=data['model'].strip(),
        year=int(data['year']),
        current_mileage=int(data['current_mileage']),
        vin=(data.get('vin') or '').strip() or None,
        notes=(data.get('notes') or '').strip() or None,
    )
    db.session.add(motorcycle)
    db.session.commit()
    return jsonify(motorcycle_to_dict(motorcycle)), 201


@motorcycles_bp.get('/<int:motorcycle_id>')
@jwt_required()
def get_motorcycle(motorcycle_id):
    motorcycle = get_owned_motorcycle_or_404(motorcycle_id)
    return jsonify(motorcycle_to_dict(motorcycle))


@motorcycles_bp.put('/<int:motorcycle_id>')
@jwt_required()
def update_motorcycle(motorcycle_id):
    motorcycle = get_owned_motorcycle_or_404(motorcycle_id)
    data = request.get_json() or {}

    for field in ['nickname', 'make', 'model', 'vin', 'notes']:
        if field in data:
            setattr(motorcycle, field, data[field].strip() if isinstance(data[field], str) else data[field])

    for field in ['year', 'current_mileage']:
        if field in data and data[field] not in [None, '']:
            setattr(motorcycle, field, int(data[field]))

    db.session.commit()
    return jsonify(motorcycle_to_dict(motorcycle))


@motorcycles_bp.delete('/<int:motorcycle_id>')
@jwt_required()
def delete_motorcycle(motorcycle_id):
    motorcycle = get_owned_motorcycle_or_404(motorcycle_id)
    db.session.delete(motorcycle)
    db.session.commit()
    return jsonify({'message': 'Motorcycle deleted successfully.'})
