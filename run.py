from flask import render_template
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click
from app import create_app, db, bcrypt
from app.models import User

app = create_app()
migrate = Migrate(app, db)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')


# Flask CLI seed command
@click.command('seed')
def seed():
    """Seed the database with initial data."""
    from app.models import User, Stock, Portfolio, Transaction
    from app import bcrypt

    print("Seeding database...")

    db.drop_all()
    db.create_all()

    # Users
    user1 = User(
        full_name="Alice Johnson",
        username="alice123",
        email="alice@example.com",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )
    user2 = User(
        full_name="Bob Smith",
        username="bob_smith",
        email="bob@example.com",
        password_hash=bcrypt.generate_password_hash("securepass").decode("utf-8")
    )

    # Stocks
    stock1 = Stock(company_name="Apple Inc.", ticker="AAPL", price=175.2, volume=50000000)
    stock2 = Stock(company_name="Tesla, Inc.", ticker="TSLA", price=250.8, volume=60000000)
    stock3 = Stock(company_name="Amazon.com, Inc.", ticker="AMZN", price=135.5, volume=40000000)

    # Portfolios
    portfolio1 = Portfolio(user=user1, stock=stock1, quantity=10)
    portfolio2 = Portfolio(user=user2, stock=stock2, quantity=5)

    # Transactions
    transaction1 = Transaction(user=user1, stock=stock1, quantity=10, price=170.0, type="buy")
    transaction2 = Transaction(user=user2, stock=stock2, quantity=5, price=240.0, type="buy")
    transaction3 = Transaction(user=user1, stock=stock3, quantity=3, price=130.0, type="buy")

    db.session.add_all([
        user1, user2,
        stock1, stock2, stock3,
        portfolio1, portfolio2,
        transaction1, transaction2, transaction3
    ])
    db.session.commit()

    print("✅ Database seeded successfully!")


# Register CLI command
app.cli.add_command(seed)


if __name__ == '__main__':
    app.run(debug=True)
