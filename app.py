import os
from flask import Flask, render_template
from extensions import db, login_manager, migrate
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from models.user import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Secret key
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "devkey123")

    # Database URL: use Render's DATABASE_URL if available, otherwise local fallback
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:admin123@localhost/exam_portal"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    # Landing page
    @app.route("/")
    def index():
        return render_template("landing.html")

    return app


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # create tables if not exists
    app.run(debug=True)
