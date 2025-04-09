# tests/conftest.py
import os
import pytest
from src import create_app, mongo

@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["MONGO_DB_NAME"] = "test_mydb"
    yield

@pytest.fixture
def app(set_test_env):
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):  # Ensure app is initialized before accessing mongo.cx
    return mongo.cx["test_mydb"]
