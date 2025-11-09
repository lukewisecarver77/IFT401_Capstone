from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.market_service import create_stock

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/ping")
@login_required
def ping():
    return jsonify({"admin": True})


@admin_bp.post("/create_stock")
@login_required
def create_stock_route():
    """Admin route to create a new stock."""
    # Ensure the user is an admin
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    company_name = data.get("company_name")
    ticker = data.get("ticker")
    volume = data.get("volume")
    initial_price = data.get("initial_price")

    response, status = create_stock(company_name, ticker, volume, initial_price)
    return jsonify(response), status