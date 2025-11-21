from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.market_service import create_stock, update_market_hours, update_market_schedule, get_market_settings
from app.models import db, Stock

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Administrator Routes for Admin Functions

#Forgot the admin checks i had in here and ended up doing it through the JS file, whoops

@admin_bp.get("/ping")
#@login_required
def ping():
    """Simple check for admin access"""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403
    return jsonify({"admin": True})

@admin_bp.post("/create_stock")
#@login_required
def create_stock_route():
    """Admin route to create a new stock."""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    company_name = data.get("company_name")
    ticker = data.get("ticker")
    volume = data.get("volume")
    initial_price = data.get("initial_price")

    response, status = create_stock(company_name, ticker, volume, initial_price)
    return jsonify(response), status

@admin_bp.delete("/delete_stock/<ticker>")
#@login_required
def delete_stock_route(ticker):
    """Delete a stock by ticker."""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

    stock = Stock.query.filter_by(ticker=ticker.upper()).first()
    if not stock:
        return jsonify({"error": f"No stock found with ticker {ticker}."}), 404

    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": f"Stock {ticker.upper()} deleted successfully."})


@admin_bp.post("/update_market_hours")
#@login_required
def update_market_hours_route():
    """Admin route to update market open and close times."""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

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
#@login_required
def update_market_schedule_route():
    """Admin route to update market weekdays/holidays."""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    weekdays_only = data.get("weekdays_only")
    holidays = data.get("holidays", None)

    response, status = update_market_schedule(weekdays_only, holidays)
    return jsonify(response), status

@admin_bp.get("/stocks")
#@login_required
def get_stocks():
    """Return all stocks for admin table."""
   # if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

    stocks = Stock.query.all()
    stock_list = [
        {
            "company_name": s.company_name,
            "ticker": s.ticker,
            "volume": s.volume,
            "price": s.price
        } for s in stocks
    ]
    return jsonify({"stocks": stock_list})

@admin_bp.get("/market_settings")
def get_market_settings_route():
    """Return current market hours and schedule."""
    settings = get_market_settings()
    
    return jsonify({
        "open_time": settings.open_time.strftime('%H:%M') if settings.open_time else None,
        "close_time": settings.close_time.strftime('%H:%M') if settings.close_time else None,
        "weekdays_only": settings.weekdays_only,
        "holidays": settings.holidays
    })


@admin_bp.post("/update_stock/<ticker>")
#@login_required
def update_stock_route(ticker):
    """Update stock details: company name, ticker, volume, and price."""
    #if not current_user.is_admin:
        #return jsonify({"error": "Unauthorized: Admins only."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    company_name = data.get("company_name")
    new_ticker = data.get("ticker")
    volume = data.get("volume")
    price = data.get("price")

    if not all([company_name, new_ticker, volume, price]):
        return jsonify({"error": "All fields are required."}), 400

    stock = Stock.query.filter_by(ticker=ticker.upper()).first()
    if not stock:
        return jsonify({"error": f"No stock found with ticker {ticker}."}), 404

    try:
        stock.company_name = company_name
        stock.ticker = new_ticker.upper()
        stock.volume = int(volume)
        stock.price = float(price)
    except ValueError:
        return jsonify({"error": "Volume and price must be numeric."}), 400

    db.session.commit()

    return jsonify({
        "message": f"Stock {ticker.upper()} updated successfully.",
        "stock": {
            "company_name": stock.company_name,
            "ticker": stock.ticker,
            "volume": stock.volume,
            "price": stock.price
        }
    })
