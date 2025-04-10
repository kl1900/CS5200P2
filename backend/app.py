from src import create_app
from src.routes.auth_routes import auth_bp
from src.routes.analytics_routes import analytics_bp

app = create_app()
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(analytics_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
