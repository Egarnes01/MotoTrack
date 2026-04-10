from datetime import datetime, date
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    motorcycles = db.relationship('Motorcycle', backref='owner', lazy=True, cascade='all, delete-orphan')


class Motorcycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nickname = db.Column(db.String(120), nullable=False)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    current_mileage = db.Column(db.Integer, nullable=False, default=0)
    vin = db.Column(db.String(80))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    maintenance_logs = db.relationship('MaintenanceLog', backref='motorcycle', lazy=True, cascade='all, delete-orphan')


class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycle.id'), nullable=False)
    service_type = db.Column(db.String(120), nullable=False)
    service_date = db.Column(db.Date, nullable=False, default=date.today)
    mileage_at_service = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    cost = db.Column(db.Float, nullable=True)
    interval_miles = db.Column(db.Integer, nullable=True)
    interval_days = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def next_due_mileage(self):
        if self.interval_miles:
            return self.mileage_at_service + self.interval_miles
        return None

    def next_due_date(self):
        if self.interval_days:
            return self.service_date.fromordinal(self.service_date.toordinal() + self.interval_days)
        return None
