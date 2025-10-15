from flask import Flask
from flask_bcrypt import Bcrypt
from .database import init_db, db

bcrypt = Bcrypt()  # create bcrypt instance

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    init_db(app)
    bcrypt.init_app(app)

    # Import routes, models, etc.
    with app.app_context():
        from . import models

    return app
