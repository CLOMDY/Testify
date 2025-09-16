from flask import Flask, render_template
from extensions import db, login_manager, migrate, DB_URL
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from models.user import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load config
    app.config.from_object("config.Config")
    app.config.from_pyfile("config.py", silent=True)

    # Override DB URL from extensions (works for Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    # Landing page route
    @app.route("/")
    def index():
        return render_template("landing.html")  # shows login/register options

    return app


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()   # <-- creates all tables
    app.run(debug=True)
