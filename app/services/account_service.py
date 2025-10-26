from app.database import db
from app.models import User


def user_deposit(username):
    """Deposit funds into user account."""
    user = User.query.filter_by(username=username).first()
    try: 
        amountD = float(input("Please enter the amount you would like to deposit: "))
    except ValueError:
        print("Deposit amount must be a number.")

    if not user:
        return {'error': 'User not found.'}, 404
    
    # Ensure user has a balance attribute (if not, add one in the model)
    if not hasattr(user, 'balance'):
        return {'error': 'User balance not implemented in database.'}, 400
    
    # Add deposit amount to user balance
    user.balance += amountD

    return {'new_balance': user.balance}

def user_withdraw(username):
    """Withdraw funds from user account."""
    user = User.query.filter_by(username=username).first()
    try: 
        amountW = float(input("Please enter the amount you would like to withdraw: "))
    except ValueError:
        print("Withdrawal amount must be a number.")

    if not user:
        return {'error': 'User not found.'}, 404
    
    # Ensure user has a balance attribute (if not, add one in the model)
    if not hasattr(user, 'balance'):
        return {'error': 'User balance not implemented in database.'}, 400
    
    if user.balance < amountW:
        return {'error': 'Insufficient funds.'}, 400
    
    # Subtract withdrawal amount from user balance
    user.balance -= amountW

    return {'new_balance': user.balance}