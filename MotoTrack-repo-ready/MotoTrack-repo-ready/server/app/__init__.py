from flask import Flask, send_from_directory
from flask_cors import CORS
from .config import Config
from .extensions import db, bcrypt, jwt, migrate
from .routes.auth import auth_bp
from .routes.motorcycles import motorcycles_bp
from .routes.maintenance import maintenance_bp
from .routes.dashboard import dashboard_bp
from .models import User, Motorcycle, MaintenanceLog
import os


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(motorcycles_bp, url_prefix='/api/motorcycles')
    app.register_blueprint(maintenance_bp, url_prefix='/api/maintenance')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    with app.app_context():
        db.create_all()

    return app
