from flask import current_app

def get_db():
    db_name = current_app.config["MONGO_DB_NAME"]
    client = current_app.mongo_client
    return client[db_name]

def get_client():
    return current_app.mongo_client
