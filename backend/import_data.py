import json
import os
from pathlib import Path
from dateutil.parser import parse as parse_date

from pymongo import InsertOne, MongoClient

mongo_uri = "mongodb://mongo:27017,mongo-secondary:27017/?replicaSet=rs0"
client = MongoClient(mongo_uri)

db = client.get_database("mydb")

sample_data = Path(__file__).parent / "sample_data"

def parse_dates(doc):
    for key, value in doc.items():
        if isinstance(value, str) and "date" in key.lower() and value.endswith("Z"):
            try:
                doc[key] = parse_date(value)
            except Exception:
                pass
    return doc

for json_f in sample_data.glob("*.json"):
    collection_name = json_f.stem  # Strip extension for collection name
    collection = db[collection_name]

    with json_f.open() as f:
        data = json.load(f)

    # Accept list of docs or single doc
    docs = data if isinstance(data, list) else [data]
    docs = [parse_dates(doc) for doc in docs]
    ops = [InsertOne(doc) for doc in docs]

    if ops:
        result = collection.bulk_write(ops)
        print(f"Inserted into {collection_name}")

client.close()
# client.admin.command("ping")
