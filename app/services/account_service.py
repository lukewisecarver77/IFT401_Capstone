from app.models import db, User
from werkzeug.security import generate_password_hash

# Functions for Account actions, Deposit/Withdraw/Create Account

def user_deposit(username, amount):
    """Deposit funds into user account."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'error': 'User not found.'}, 404

    try:
        amount = float(amount)
    except ValueError:
        return {'error': 'Deposit amount must be a number.'}, 400

    if amount <= 0:
        return {'error': 'Deposit amount must be positive.'}, 400

    user.balance += amount
    db.session.commit()

    return {'new_balance': user.balance}, 200


def user_withdraw(username, amount):
    """Withdraw funds from user account."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'error': 'User not found.'}, 404

    try:
        amount = float(amount)
    except ValueError:
        return {'error': 'Withdrawal amount must be a number.'}, 400

    if amount <= 0:
        return {'error': 'Withdrawal amount must be positive.'}, 400

    if user.balance < amount:
        return {'error': 'Insufficient funds.'}, 400

    user.balance -= amount
    db.session.commit()

    return {'new_balance': user.balance}, 200


def create_user_account(full_name, username, email, password, is_admin=False):
    """Create a new user account."""

    full_name = (full_name or "").strip()
    username  = (username or "").strip().lower()
    email     = (email or "").strip().lower()

    if not all([full_name, username, email, password]):
        return {"error": "Missing required fields"}, 400

    existing = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing:
        return {"error": "Username or email already exists"}, 409

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=is_admin,
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }, 201
