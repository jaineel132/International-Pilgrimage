from flask import Flask, request, session
from config import Config
from extensions import db, migrate, login_manager, mail, csrf
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload folder exists
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)  # Initialize CSRF protection
    
    # Configure CSRF to exempt certain routes if needed
    csrf.exempt("payment.process_payment")

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from models import User
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register blueprints
        from routes import main
        from auth import auth
        from payment import payment_bp
        from trip_management import trip_bp  # New blueprint for trip management

        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(payment_bp)
        app.register_blueprint(trip_bp)  # Register the new blueprint

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

print("Advanced Flask application is ready to run!")

