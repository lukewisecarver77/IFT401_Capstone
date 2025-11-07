from flask import Blueprint, jsonify

trade_bp = Blueprint("trade", __name__, url_prefix="/trade")

@trade_bp.get("/ping")
def ping():
    return jsonify({"ok": True})
