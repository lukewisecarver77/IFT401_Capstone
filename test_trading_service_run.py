from app import create_app, db
from app.models import User, Stock, Portfolio, Transaction
from app.services.trading_service import stock_buy, stock_sell

# Initialize app context
app = create_app()
app.app_context().push()

def ensure_user_balance(user, default_balance=10000.0):
    if user.balance is None:
        user.balance = default_balance
        db.session.commit()

def print_user_portfolio(user):
    portfolios = Portfolio.query.filter_by(user_id=user.id).all()
    portfolio_str = ", ".join([f"{p.stock.ticker}: {p.quantity}" for p in portfolios]) or "Empty"
    print(f"{user.username} balance: {user.balance}, portfolio: {portfolio_str}")

def main():
    # Fetch users
    alice = User.query.filter_by(username="alice123").first()
    bob = User.query.filter_by(username="bob_smith").first()

    # Safety checks
    if alice is None or bob is None:
        raise ValueError("Test users not found in the database")

    # Ensure balances are set
    ensure_user_balance(alice)
    ensure_user_balance(bob)

    print("=== Initial State ===")
    print_user_portfolio(alice)
    print_user_portfolio(bob)

    print("\n=== Testing Buy ===")
    result = stock_buy(alice.username, "AAPL", 10)
    print(result)
    print_user_portfolio(alice)

    result = stock_buy(bob.username, "TSLA", 5)
    print(result)
    print_user_portfolio(bob)

    print("\n=== Testing Sell ===")
    result = stock_sell(alice.username, "AAPL", 5)
    print(result)
    print_user_portfolio(alice)

    result = stock_sell(bob.username, "TSLA", 2)
    print(result)
    print_user_portfolio(bob)

    print("\n=== Testing Error Cases ===")
    # Buying more than balance
    result = stock_buy(alice.username, "GOOG", 100000)
    print(result)

    # Selling more than owned
    result = stock_sell(bob.username, "TSLA", 100)
    print(result)

if __name__ == "__main__":
    main()
