from flask import Blueprint, jsonify
from app.models import Stock

market_bp = Blueprint("market", __name__, url_prefix="/market")

# Route for full-page stocks view
@market_bp.get("/stocks")
def get_stocks():
    """Return all stocks in the market for public view (full page)."""
    stocks = Stock.query.all()
    stock_list = [
        {
            "ticker": s.ticker,
            "company_name": s.company_name,
            "price": s.price,
            "volume": s.volume
        } for s in stocks
    ]
    return jsonify({"stocks": stock_list}), 200


# Route for JSON polling (used by JavaScript to update tables)
@market_bp.get("/stocks/data")
def stocks_data():
    """Return current stock data in JSON format for table refresh."""
    stocks = Stock.query.all()
    stock_list = []
    for stock in stocks:
        stock_list.append({
            "ticker": stock.ticker,
            "company_name": stock.company_name,
            "price": stock.price,
            "volume": stock.volume
        })
    return jsonify(stock_list), 200
