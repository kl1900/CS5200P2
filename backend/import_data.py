import json
import os
from pathlib import Path
from pymongo import InsertOne, MongoClient
import bcrypt

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/mydb")
client = MongoClient(mongo_uri)
db = client.get_database()

sample_data = Path(__file__).parent / "sample_data"

for json_f in sample_data.glob("*.json"):
    collection_name = json_f.stem # Strip extension for collection name

    collection = db[collection_name]

    with json_f.open() as f:
        data = json.load(f)

    if collection_name == "users":
        for user in data:
            # Hash the default password "password"
            hashed = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt())
            user["password"] = hashed.decode('utf-8')

    # Accept list of docs or single doc
    docs = data if isinstance(data, list) else [data]
    ops = [InsertOne(doc) for doc in docs]

    if ops:
        collection.bulk_write(ops)
        print(f"Inserted into {collection_name}")

client.close()
# client.admin.command("ping")
