from flask import Flask, render_template
from config import Config
from extensions import db, csrf, login_manager
from models import User, Doctor, Patient, Department, Appointment

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app); csrf.init_app(app); login_manager.init_app(app)
    from routes.main import bp as main_bp
    from routes.auth import bp as auth_bp
    from routes.admin import bp as admin_bp
    from routes.doctor import bp as doctor_bp
    from routes.patient import bp as patient_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")
    app.register_blueprint(patient_bp, url_prefix="/patient")
    @app.errorhandler(403)
    def forbidden(e): return render_template("errors/403.html"), 403
    @app.errorhandler(404)
    def missing(e): return render_template("errors/404.html"), 404
    @app.errorhandler(500)
    def failed(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500
    return app
