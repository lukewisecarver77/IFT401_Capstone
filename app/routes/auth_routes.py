from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    full_name = (data.get("full_name") or "").strip()
    username  = (data.get("username") or "").strip().lower()
    email     = (data.get("email") or "").strip().lower()
    password  = data.get("password") or ""
    if not all([full_name, username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    if User.query.filter((User.username==username)|(User.email==email)).first():
        return jsonify({"error": "Username or email already exists"}), 409
    user = User(full_name=full_name, username=username, email=email,
                password_hash=generate_password_hash(password))
    db.session.add(user); db.session.commit()
    return jsonify({"message":"Registered","user":{"id":user.id,"username":user.username}}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    ident = (data.get("username") or data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not ident or not password:
        return jsonify({"error":"Missing credentials"}), 400
    user = User.query.filter((User.username==ident)|(User.email==ident)).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error":"Invalid username/email or password"}), 401
    login_user(user)
    return jsonify({"message":"Logged in","user":{"id":user.id,"username":user.username}}), 200

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logged out"}), 200

@auth_bp.get("/me")
@login_required
def me():
    return jsonify({"id":current_user.id,"username":current_user.username,"email":current_user.email}), 200
