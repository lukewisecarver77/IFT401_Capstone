from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.market_service import create_stock, update_market_hours, update_market_schedule

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.get("/ping")
@login_required
def ping():
    """Simple check for admin access"""
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized: Admins only."}), 403
    return jsonify({"admin": True})

@admin_bp.post("/create_stock")
@login_required
def create_stock_route():
    """Admin route to create a new stock."""
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

@admin_bp.post("/update_market_hours")
@login_required
def update_market_hours_route():
    """Admin route to update market open and close times."""
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    open_hour = data.get("open_hour")
    open_minute = data.get("open_minute")
    close_hour = data.get("close_hour")
    close_minute = data.get("close_minute")

    response, status = update_market_hours(open_hour, open_minute, close_hour, close_minute)
    return jsonify(response), status

@admin_bp.post("/update_market_schedule")
@login_required
def update_market_schedule_route():
    """Admin route to update market weekdays/holidays."""
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    weekdays_only = data.get("weekdays_only")
    holidays = data.get("holidays", None)

    response, status = update_market_schedule(weekdays_only, holidays)
    return jsonify(response), status
