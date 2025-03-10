from flask import Flask, send_from_directory
from config import Config
from extensions import db, migrate, login_manager

from routes import main
from auth import auth

from models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    with app.app_context():
        
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        
        app.register_blueprint(main)
        app.register_blueprint(auth)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

print("Running!!")

