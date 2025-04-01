from flask import Flask
from src.extensions import mongo
from src.routes.user_routes import user_bp
import os

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mydb')

    mongo.init_app(app)
    
    @app.route("/")
    def index():
        return "Flask MongoDB API is running 🚀", 200

    app.register_blueprint(user_bp, url_prefix="/users")

    return app
