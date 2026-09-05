import os
from flask import Flask, redirect, url_for, render_template
from flask_login import current_user
from config import config_by_name
from app.extensions import db, login_manager, csrf

def create_app(config_name: str | None = None) -> Flask:
    """
    Application Factory pattern implementation.
    Registers Blueprints, Extensions, and Centralized Error Handlers.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__, instance_relative_config=True)
    
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        from app.models import User
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.faculty import faculty_bp
    from app.routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(student_bp)

    # Root route redirection
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif current_user.role == "faculty":
                return redirect(url_for("faculty.dashboard"))
            elif current_user.role == "student":
                return redirect(url_for("student.dashboard"))
        return redirect(url_for("auth.login"))

    # Health check route
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "phase": "Phase 2 - Authentication & RBAC Active",
            "database": app.config["SQLALCHEMY_DATABASE_URI"].split("://")[0]
        }

    # Centralized HTTP Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        return render_template("errors/403.html", error_code=400, error_message="Bad Request or CSRF token validation failed."), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html", error_code=403, error_message="Access Forbidden: You do not have permission to access this resource."), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", error_code=404, error_message="Page Not Found: The requested resource does not exist."), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("errors/500.html", error_code=500, error_message="Internal Server Error: An unexpected issue occurred on the server."), 500

    return app