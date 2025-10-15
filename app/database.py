from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance
db = SQLAlchemy()

# Optional helper function to initialize with Flask app
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Creates tables for all models that will be defined
