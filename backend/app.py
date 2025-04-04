from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SECRET_KEY = "your-secret-key"

client = MongoClient("mongodb://mongo:27017/mydb")
db = client.get_database()

def token_required(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').split('Bearer ')[-1]
            if not token:
                return jsonify({"error": "Token missing"}), 401
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if permission not in data['permissions']:
                    return jsonify({"error": "Not authorized"}), 403
            except Exception as e:
                return jsonify({"error": str(e)}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = db.users.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        permissions = db.permissions.find_one()['permissions'][user['roles']]
        payload = {
            "user_id": user["user_id"],
            "email": user["email"],
            "roles": user["roles"],
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/products', methods=['GET', 'OPTIONS'])
def get_products():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({}), 200
    try:
        products = list(db.products.find({}, {"_id": 0}))
        return jsonify(products), 200
    except Exception as e:
        app.logger.error(f"Error fetching products: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
