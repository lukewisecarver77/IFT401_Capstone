from run import app        
from app.database import db
from app.models import User, Stock
from run import bcrypt      

with app.app_context():
    
    db.drop_all()
    db.create_all()

    # --- Seed Users ---
    users = [
        {"full_name": "Alice", "username": "alice123", "email": "alice@example.com", "password": "alice_password", "is_admin": False},
        {"full_name": "Bob", "username": "bob456", "email": "bob@example.com", "password": "bob_password", "is_admin": False},
        {"full_name": "Admin", "username": "admin", "email": "admin@example.com", "password": "admin_password", "is_admin": True},
    ]

    for u in users:
        hashed_pw = bcrypt.generate_password_hash(u["password"]).decode("utf-8")
        user = User(full_name=u["full_name"], username=u["username"], email=u["email"], password_hash=hashed_pw, is_admin=u["is_admin"])
        db.session.add(user)

    # --- Seed Stocks ---
    stocks = [
        {"company_name": "Acme Corp", "ticker": "ACME", "price": 100.0, "volume": 10000},
        {"company_name": "Globex", "ticker": "GLBX", "price": 50.0, "volume": 5000},
    ]

    for s in stocks:
        stock = Stock(company_name=s["company_name"], ticker=s["ticker"], price=s["price"], volume=s["volume"])
        db.session.add(stock)

    db.session.commit()
    print("Database seeded successfully!")
