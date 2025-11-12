from flask import Blueprint, jsonify
from app.models import Stock

market_bp = Blueprint("market", __name__, url_prefix="/market")

@market_bp.get("/stocks")
def get_stocks():
    """Return all stocks in the market for public view."""
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
