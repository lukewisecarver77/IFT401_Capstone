from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.services.trading_service import (
    stock_buy,
    stock_sell,
    view_portfolio,
    view_transactions
)
from app.models import Stock

# Routes for Stock Trading

trade_bp = Blueprint("trade", __name__, url_prefix="/trade")


@trade_bp.get("/ping")
def ping():
    return jsonify({"ok": True})


@trade_bp.post("/buy")
@login_required
def buy_stock():
    data = request.get_json(silent=True) or {}
    ticker = (data.get("ticker") or "").strip().upper()
    quantity = data.get("quantity")

    if not ticker or quantity is None:
        return jsonify({"error": "Ticker and quantity are required"}), 400

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be an integer"}), 400

    try:
        result = stock_buy(current_user.username, ticker, quantity)
        return jsonify(result), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # unexpected server error
        # in production log the exception
        return jsonify({"error": "Internal server error"}), 500


@trade_bp.post("/sell")
@login_required
def sell_stock():
    data = request.get_json(silent=True) or {}
    ticker = (data.get("ticker") or "").strip().upper()
    quantity = data.get("quantity")

    if not ticker or quantity is None:
        return jsonify({"error": "Ticker and quantity are required"}), 400

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity must be an integer"}), 400

    try:
        result = stock_sell(current_user.username, ticker, quantity)
        return jsonify(result), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        # in production log the exception
        return jsonify({"error": "Internal server error"}), 500


@trade_bp.get("/portfolio")
@login_required
def get_portfolio():
    try:
        portfolio = view_portfolio(current_user.username)
        return jsonify({"portfolio": portfolio}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@trade_bp.get("/transactions")
@login_required
def get_transactions():
    try:
        transactions = view_transactions(current_user.username)
        return jsonify({"transactions": transactions}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@trade_bp.get("/stocks")
def market_stocks():
    """Public endpoint for all market stocks."""
    stocks = Stock.query.all()
    result = []
    for s in stocks:
        result.append({
            "ticker": s.ticker,
            "company_name": s.company_name,
            "price": s.price,
            "volume": s.volume
        })
    return jsonify({"stocks": result}), 200
