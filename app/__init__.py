from flask import Flask
from app.extension import db, login_manager, migrate, babel, csrf
from app.models.user import User
from app.auth.routes import auth
from app.routes import main
from dotenv import load_dotenv
from config import Config
from flask_socketio import SocketIO
from app.sockets import register_socketio_events
from app.api.routes import api
from app.dashboard.routes import dashboard

load_dotenv()

# --- Initialize extensions globally
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    migrate.init_app(app, db)
    babel.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)

    # Register socket events
    register_socketio_events(socketio)

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(dashboard)

    # Database setup
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
