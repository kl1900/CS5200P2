"pytest configuration"

import os

import pytest

from src import create_app
from src.db import get_db


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["MONGO_DB_NAME"] = "test_mydb"
    yield


@pytest.fixture(scope="session", autouse=True)
def app(set_test_env):
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    with app.app_context():
        from src.db import get_db
        return get_db()

@pytest.fixture(scope="function", autouse=True)
def clean_db(db):
    yield
    for name in db.list_collection_names():
        db.drop_collection(name)
