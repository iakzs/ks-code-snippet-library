from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug import security
from app.utils.security import safe_str_cmp

security.safe_str_cmp = safe_str_cmp

from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.snippets import bp as snippets_bp
    app.register_blueprint(snippets_bp, url_prefix='/snippets')

    return app

from app import models
