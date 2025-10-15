import os

# Get the absolute path of the project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Use DATABASE_URL environment variable if set (for deployment), otherwise use SQLite in instance folder
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'instance', 'stock_trading.db')}"
    
    # Turn off modification tracking for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Optional: Secret key for sessions, forms, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-change-this'

