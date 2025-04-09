import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.extensions import mongo
from src.routes.cart_routes import cart_bp
from src.routes.checkout_routes import checkout_bp
from src.routes.order_routes import order_bp
# Import all your blueprints
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)

    # Default to 'mydb', or override with test env in tests
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    db_name = os.environ.get("MONGO_DB_NAME", "mydb")

    app.config["MONGO_URI"] = f"{mongo_uri}{db_name}?replicaSet=rs0"

    mongo.init_app(app)

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
    app.register_blueprint(checkout_bp)

    return app
