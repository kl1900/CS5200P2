from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from src.extensions import mongo

# Import all your blueprints
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp
from src.routes.cart_routes import cart_bp
from src.routes.order_routes import order_bp

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get(
        "MONGO_URI", "mongodb://localhost:27017/mydb"
    )
    
    mongo.init_app(app)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Handle OPTIONS requests (preflight)
    @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
    @app.route('/<path:path>', methods=['OPTIONS'])
    def options_handler(path):
        return '', 200
    
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
    
    return app