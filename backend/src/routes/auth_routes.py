from flask import Blueprint, request, jsonify
from src.models.user_model import find_user_by_email
import jwt
import datetime
import os

# get a JWT token
auth_bp = Blueprint("auth", __name__)
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    user = find_user_by_email(email)

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = jwt.encode({
        "user_id": user["user_id"],
        "email": user["email"],
        "roles": user["roles"],  # e.g., "admin", "buyer", "seller"
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})

