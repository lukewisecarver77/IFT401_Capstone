from app.database import db
from app.models import User, Stock, Portfolio, Transaction


def stock_price(ticker):
    """Get the current price of a stock by ticker symbol."""
    stock = Stock.query.filter_by(ticker=ticker).first()
    if stock and stock.price:
        return stock.price
    raise ValueError(f"Unable to fetch price for {ticker}")


def stock_buy(username, ticker, quantity):
    """Handle buying stocks for a user."""
    user = User.query.filter_by(username=username).first()
    stock = Stock.query.filter_by(ticker=ticker).first()

    if not user:
        return {'error': 'User not found.'}, 404
    if not stock:
        return {'error': 'Stock not found.'}, 404

    price_current = stock_price(ticker)
    total_cost = price_current * quantity

    # Ensure user has a balance attribute (if not, add one in the model)
    if not hasattr(user, 'balance'):
        return {'error': 'User balance not implemented in database.'}, 400

    if user.balance < total_cost:
        return {'error': 'Insufficient funds.'}, 400

    # Deduct balance and update portfolio
    user.balance -= total_cost

    portfolio = Portfolio.query.filter_by(user_id=user.id, stock_id=stock.id).first()
    if portfolio:
        portfolio.quantity += quantity
    else:
        portfolio = Portfolio(user_id=user.id, stock_id=stock.id, quantity=quantity)
        db.session.add(portfolio)

    # Record transaction
    transaction = Transaction(
        user_id=user.id,
        stock_id=stock.id,
        quantity=quantity,
        price=price_current,
        type='buy'
    )

    db.session.add(transaction)
    db.session.commit()

    return {
        'message': f"Bought {quantity} shares of {ticker} at ${price_current:.2f} each.",
        'new_balance': user.balance
    }


def stock_sell(username, ticker, quantity):
    """Handle selling stocks for a user."""
    user = User.query.filter_by(username=username).first()
    stock = Stock.query.filter_by(ticker=ticker).first()

    if not user:
        return {'error': 'User not found.'}, 404
    if not stock:
        return {'error': 'Stock not found.'}, 404

    portfolio = Portfolio.query.filter_by(user_id=user.id, stock_id=stock.id).first()
    if not portfolio or portfolio.quantity < quantity:
        return {'error': 'Not enough shares to sell.'}, 400

    price_current = stock_price(ticker)
    total_sale = price_current * quantity

    # Deduct shares
    portfolio.quantity -= quantity
    if portfolio.quantity == 0:
        db.session.delete(portfolio)

    # Credit user balance
    user.balance += total_sale

    # Record transaction
    transaction = Transaction(
        user_id=user.id,
        stock_id=stock.id,
        quantity=quantity,
        price=price_current,
        type='sell'
    )

    db.session.add(transaction)
    db.session.commit()

    return {
        'message': f"Sold {quantity} shares of {ticker} at ${price_current:.2f} each.",
        'new_balance': user.balance
    }

def view_portfolio(username):
    """Display portfolio of a user."""
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'User not found.'}, 404
    
    portfolio = Portfolio.query.filter_by(user_id=user.id)
    if portfolio:
        return {portfolio}
    else:
        return {'error': 'Portfolio not found'}, 404
    
def view_transactions(username):
    """Display user transactions."""
    user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'User not found.'}, 404
    
    transactions = Transaction.query.filter_by(user_id=user.id)
    if transactions:
        return {transactions}
    else:
        return {'error': 'No transactions found for user.'}, 404