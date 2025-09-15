from flask import Flask, render_template
from extensions import db, login_manager
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from models.user import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    # Init extensions
    db.init_app(app)
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
        return render_template("landing.html")

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()   # fine for now, switch to migrations later
    app.run(debug=True)
