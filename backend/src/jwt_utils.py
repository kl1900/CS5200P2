from flask import request, jsonify
import jwt
import os
from functools import wraps

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")

permissions = {
    "buyer": ["view_products", "make_purchase"],
    "seller": ["view_products", "list_product", "edit_product", "delete_product"],
    "admin": ["view_products", "edit_product", "delete_product", "delete_user", "manage_roles"]
}

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated

def role_required(required_permission):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                return jsonify({"error": "Token missing"}), 401
            try:
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                role = decoded.get("roles")
                if role not in permissions or required_permission not in permissions[role]:
                    return jsonify({"error": "Permission denied"}), 403
                request.user = decoded
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 403
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper