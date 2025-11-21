from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.services.account_service import user_deposit, user_withdraw
from app.services.trading_service import view_portfolio, view_transactions

user_bp = Blueprint("user", __name__, url_prefix="/users")

# User Account Routes

@user_bp.get("/me")
@login_required
def whoami():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
        "is_admin": current_user.is_admin
    }), 200

@user_bp.get("/<username>/portfolio")
def get_portfolio(username):
    try:
        portfolio = view_portfolio(username)
        return jsonify({"portfolio": portfolio}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@user_bp.get("/<username>/transactions")
def get_user_transactions(username):
    try:
        transactions = view_transactions(username)
        return jsonify({"transactions": transactions}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@user_bp.post("/me/deposit")
@login_required
def deposit():
    data = request.get_json() or {}
    amount = data.get("amount")
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    response, status = user_deposit(current_user.username, amount)
    return jsonify(response), status

@user_bp.post("/me/withdraw")
@login_required
def withdraw():
    data = request.get_json() or {}
    amount = data.get("amount")
    if amount is None:
        return jsonify({"error": "Amount is required"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    response, status = user_withdraw(current_user.username, amount)
    return jsonify(response), status
