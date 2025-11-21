from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from sqlalchemy.types import JSON
from datetime import datetime,timezone, time
from sqlalchemy import text



db = SQLAlchemy()

# User DB Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=10000.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    portfolios = db.relationship("Portfolio", backref="user", lazy=True)
    transactions = db.relationship("Transaction", backref="user", lazy=True)

# Stock DB Model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    high = db.Column(db.Float, nullable=True)
    low = db.Column(db.Float, nullable=True)
    market_cap = db.Column(db.Float, nullable=True)

    portfolios = db.relationship("Portfolio", backref="stock", lazy=True)
    transactions = db.relationship("Transaction", backref="stock", lazy=True)

# Portfolio DB Model
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Trasaction DB Mode
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Market Settings DB Model
class MarketSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    open_time = db.Column(db.Time, nullable=False, server_default=text("'09:00:00'"))
    close_time = db.Column(db.Time, nullable=False, server_default=text("'16:00:00'"))
    weekdays_only = db.Column(db.Boolean, default=True)
    holidays = db.Column(JSON, default=[])