from src import create_app
from src.routes.auth_routes import auth_bp
app = create_app()
app.register_blueprint(auth_bp, url_prefix="/auth")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
