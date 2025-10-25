from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .database import init_db, db

bcrypt = Bcrypt()
migrate = Migrate()  # Add migrate instance

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    init_db(app)        # This should init db (SQLAlchemy)
    bcrypt.init_app(app)
    migrate.init_app(app, db)  # <-- initialize Flask-Migrate

    # Import routes, models, etc.
    with app.app_context():
        from . import models

    return app
