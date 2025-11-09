from app.models import db, Stock, MarketSettings
from datetime import time

def create_stock(company_name, ticker, volume, initial_price):
    """Create a new stock entry (admin function)."""
    existing_stock = Stock.query.filter_by(ticker=ticker).first()
    if existing_stock:
        return {'error': 'A stock with this ticker already exists.'}, 400

    try:
        volume = int(volume)
        initial_price = float(initial_price)
    except ValueError:
        return {'error': 'Volume and price must be numeric.'}, 400

    if volume <= 0 or initial_price <= 0:
        return {'error': 'Volume and price must be positive values.'}, 400

    new_stock = Stock(
        company_name=company_name,
        ticker=ticker.upper(),
        volume=volume,
        price=initial_price
    )

    db.session.add(new_stock)
    db.session.commit()

    return {
        'message': f'Stock {ticker.upper()} ({company_name}) created successfully.',
        'stock': {
            'company_name': company_name,
            'ticker': ticker.upper(),
            'volume': volume,
            'price': initial_price
        }
    }, 201

def get_market_settings():
    """Create/Retrieve MarketSettings Record."""
    settings = MarketSettings.query.first()
    if not settings:
        settings = MarketSettings()
        db.session.add(settings)
        db.session.commit()
    return settings


def update_market_hours(open_hour, open_minute, close_hour, close_minute):
    """Update market open and close times."""
    settings = get_market_settings()

    try:
        new_open = time(int(open_hour), int(open_minute))
        new_close = time(int(close_hour), int(close_minute))
    except ValueError:
        return {'error': 'Invalid time format. Please use integers for hours and minutes.'}, 400

    if new_open >= new_close:
        return {'error': 'Open time must be before close time.'}, 400

    settings.open_time = new_open
    settings.close_time = new_close
    db.session.commit()

    return {
        'message': 'Market hours updated successfully.',
        'open_time': settings.open_time.strftime('%H:%M'),
        'close_time': settings.close_time.strftime('%H:%M')
    }, 200


def update_market_schedule(weekdays_only, holidays=None):
    """Update market schedule."""
    settings = get_market_settings()

    if not isinstance(weekdays_only, bool):
        return {'error': 'weekdays_only must be a boolean value.'}, 400

    settings.weekdays_only = weekdays_only

    if holidays is not None:
        if not isinstance(holidays, list):
            return {'error': 'holidays must be a list of strings (dates).'}, 400
        settings.holidays = holidays

    db.session.commit()

    return {
        'message': 'Market schedule updated successfully.',
        'weekdays_only': settings.weekdays_only,
        'holidays': settings.holidays
    }, 200