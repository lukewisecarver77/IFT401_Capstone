from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db, User

# Blueprints
from .routes.admin_routes import admin_bp
from .routes.auth_routes import auth_bp
from .routes.user_routes import user_bp
from .routes.trade_routes import trade_bp
from .routes.market_routes import market_bp
from .routes.page_routes import page_bp

login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(page_bp)

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    return app
