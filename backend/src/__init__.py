import os

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from src.routes.cart_routes import cart_bp
from src.routes.api_routes import api_bp
from src.routes.order_routes import order_bp
# Import all your blueprints
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp
from pymongo import MongoClient

mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017,mongo-secondary:27017/?replicaSet=rs0")
mongo_client = MongoClient(mongo_uri)

def create_app():
    app = Flask(__name__)
    app.config["MONGO_DB_NAME"] = os.getenv("MONGO_DB_NAME", "mydb")
    app.mongo_client = mongo_client

    # Enable CORS for all routes
    CORS(app)

    # Add CORS headers directly to every response
    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    #     response.headers.add('Access-Control-Allow-Credentials', 'true')
    #     return response

    # Handle OPTIONS requests (preflight)
    @app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
    @app.route("/<path:path>", methods=["OPTIONS"])
    def options_handler(path):
        return "", 200

    @app.route("/")
    def index():
        return "Flask MongoDB API is running 🚀", 200

    # Test route to check CORS
    @app.route("/test-cors", methods=["GET"])
    def test_cors():
        return jsonify({"message": "CORS is working!"}), 200

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(cart_bp, url_prefix="/carts")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(api_bp)

    return app
