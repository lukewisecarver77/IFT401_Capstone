from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

page_bp = Blueprint("pages", __name__)

# HTML Page Routes

@page_bp.get("/")
def index():
    return render_template("index.html")

@page_bp.get("/login")
def login_page():
    return render_template("login.html")

@page_bp.get("/register")
def register_page():
    return render_template("register.html")

@page_bp.get("/portfolio")
@login_required
def portfolio_page():
    return render_template("portfolio.html")

@page_bp.get("/transactions")
@login_required
def transactions_page():
    return render_template("transactions.html")

@page_bp.get("/trade")
@login_required
def trade_page():
    return render_template("trade.html")

@page_bp.get("/deposit_withdraw")
@login_required
def deposit_withdraw_page():
    return render_template("deposit_withdraw.html")

@page_bp.get("/admin")
@login_required
def admin_page():
    if not current_user.is_admin:
        flash("You're not an admin, can't access admin page", "error")
        return redirect(url_for("pages.index"))
    return render_template("admin.html")
