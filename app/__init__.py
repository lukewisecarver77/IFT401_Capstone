from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db, User
from app.routes.admin_routes import admin_bp
from .routes.market_routes import market_bp

login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(market_bp)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Frontend routes
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/portfolio")
    def portfolio_page():
        return render_template("portfolio.html")

    @app.route("/trade")
    def trade_page():
        return render_template("trade.html")

    @app.route("/transactions")
    def transactions_page():
        return render_template("transactions.html")

    @app.route("/deposit_withdraw")
    def deposit_withdraw_page():
        return render_template("deposit_withdraw.html")

    @app.route("/admin")
    def admin_page():
        return render_template("admin.html")

    # Backend routes
    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.trade_routes import trade_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trade_bp)
    app.register_blueprint(admin_bp)

    return app
