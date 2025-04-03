import os

from flask import Flask
from flask_cors import CORS

from src.extensions import mongo
from src.routes.cart_routes import cart_bp
from src.routes.order_routes import order_bp
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get(
        "MONGO_URI", "mongodb://localhost:27017/mydb"
    )

    mongo.init_app(app)

    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    @app.route("/")
    def index():
        return "Flask MongoDB API is running 🚀", 200

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(cart_bp, url_prefix="/carts")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(order_bp, url_prefix="/orders")

    return app
