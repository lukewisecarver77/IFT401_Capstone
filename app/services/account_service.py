from app.database import db
from app.models import User

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
