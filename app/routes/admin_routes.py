from flask import Blueprint, jsonify
from flask_login import login_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.get("/ping")
@login_required
def ping():
    return jsonify({"admin": True})
