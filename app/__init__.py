from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db, User
from app.routes.admin_routes import admin_bp

login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.get("/")
    def index():
        return {"status": "ok"}

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.trade_routes import trade_bp
    from .routes.admin_routes import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(admin_bp)

    return app
