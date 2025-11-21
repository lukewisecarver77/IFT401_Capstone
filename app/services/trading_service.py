# app/services/trading_service.py
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.models import db, User, Stock, Portfolio, Transaction

# Functions for Trading Actions for Accounts (had to add some extra to get things to work)

def _get_user_by_username(username: str) -> User:
    user = User.query.filter_by(username=username).first()
    if not user:
        raise LookupError("User not found.")
    return user

def _get_stock_by_ticker(ticker: str) -> Stock:
    stock = Stock.query.filter_by(ticker=ticker).first()
    if not stock:
        raise LookupError("Stock not found.")
    return stock

def stock_price(ticker: str) -> float:
    stock = _get_stock_by_ticker(ticker)
    if stock.price is None:
        raise ValueError(f"Price not available for {ticker}")
    return stock.price





# Project Required Functions Below





def stock_buy(username: str, ticker: str, quantity: int) -> Dict[str, Any]:
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    user = _get_user_by_username(username)
    stock = _get_stock_by_ticker(ticker)

    if stock.volume is None:
        raise ValueError("Stock volume unavailable.")
    if stock.volume < quantity:
        raise ValueError("Not enough market volume available to buy.")

    price_current = stock_price(ticker)
    total_cost = price_current * quantity

    if user.balance < total_cost:
        raise ValueError("Insufficient funds.")

    user.balance -= total_cost
    stock.volume -= quantity

    portfolio = Portfolio.query.filter_by(user_id=user.id, stock_id=stock.id).first()
    if portfolio:
        portfolio.quantity += quantity
    else:
        portfolio = Portfolio(user_id=user.id, stock_id=stock.id, quantity=quantity)
        db.session.add(portfolio)

    transaction = Transaction(
        user_id=user.id,
        stock_id=stock.id,
        quantity=quantity,
        price=price_current,
        type="buy",
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(transaction)

    db.session.commit()

    return {
        "message": f"Bought {quantity} shares of {ticker} at ${price_current:.2f} each.",
        "new_balance": user.balance
    }


def stock_sell(username: str, ticker: str, quantity: int) -> Dict[str, Any]:
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    user = _get_user_by_username(username)
    stock = _get_stock_by_ticker(ticker)

    portfolio = Portfolio.query.filter_by(user_id=user.id, stock_id=stock.id).first()
    if not portfolio or portfolio.quantity < quantity:
        raise ValueError("Not enough shares to sell.")

    price_current = stock_price(ticker)
    total_sale = price_current * quantity

    portfolio.quantity -= quantity
    if portfolio.quantity == 0:
        db.session.delete(portfolio)

    user.balance += total_sale
    if stock.volume is None:
        stock.volume = 0
    stock.volume += quantity

    transaction = Transaction(
        user_id=user.id,
        stock_id=stock.id,
        quantity=quantity,
        price=price_current,
        type="sell",
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(transaction)

    db.session.commit()

    return {
        "message": f"Sold {quantity} shares of {ticker} at ${price_current:.2f} each.",
        "new_balance": user.balance
    }


def view_portfolio(username: str) -> List[Dict[str, Any]]:
    user = _get_user_by_username(username)
    portfolio_items = Portfolio.query.filter_by(user_id=user.id).all()
    result = []
    for p in portfolio_items:
        result.append({
            "ticker": p.stock.ticker,
            "company_name": p.stock.company_name,
            "quantity": p.quantity,
            "current_price": p.stock.price,
            "total_value": (p.quantity * p.stock.price) if p.stock.price is not None else None
        })
    return result


def view_transactions(username: str) -> List[Dict[str, Any]]:
    user = _get_user_by_username(username)
    transactions = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    result = []
    for t in transactions:
        result.append({
            "ticker": t.stock.ticker,
            "company_name": t.stock.company_name,
            "quantity": t.quantity,
            "price": t.price,
            "type": t.type,
            "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return result
