from flask import Blueprint, jsonify
from flask_login import login_required, current_user

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.get("/me")
@login_required
def whoami():
    return jsonify({"id": current_user.id, "username": current_user.username})
