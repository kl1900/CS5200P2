import random
from datetime import datetime, timedelta
from pymongo import MongoClient
import time

# === Configuration and Connection ===
client = MongoClient("mongodb://mongo:27017,mongo-secondary:27017/?replicaSet=rs0")
db = client["mydb"]

# Collections
orders_collection = db["orders"]
users_collection = db["users"]
products_collection = db["products"]

# === Get Valid User IDs from the Existing Users Collection ===
valid_user_ids = [user["user_id"] for user in users_collection.find({}, {"user_id": 1, "_id": 0})]
if not valid_user_ids:
    raise Exception("No valid users found in the database. Please populate the users collection first.")

# === Clear Existing Orders (For a Clean Benchmark Test) ===
orders_collection.delete_many({})
print("Existing orders cleared.")

# === Define Sample Product IDs ===
product_ids = [
    "prod_00123", "prod_00001", "prod_00002", "prod_00003", "prod_00004",
    "prod_00005", "prod_00006", "prod_00007", "prod_00008", "prod_00009",
    "prod_00010", "prod_00011", "prod_00012", "prod_00013", "prod_00014",
    "prod_00015", "prod_00016", "prod_00017", "prod_00018", "prod_00019"
]

# === Generate Fake Orders ===
NUM_ORDERS = 100000  # Increase this number to simulate more load
orders = []
for order_num in range(1, NUM_ORDERS + 1):
    num_items = random.randint(1, 5)  # Each order will have between 1 and 5 items
    items = []
    for _ in range(num_items):
        prod_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10, 500), 2)
        item = {
            "product_id": prod_id,
            "name": f"Product for {prod_id}",  # For simulation purposes
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": round(unit_price * quantity, 2)
        }
        items.append(item)
    
    order = {
        "order_id": f"order_{order_num:05d}",
        "user_id": random.choice(valid_user_ids),  # Use a valid user id from DB
        "items": items,
        "subtotal": round(sum(item["subtotal"] for item in items), 2),
        "tax": round(random.uniform(5, 20), 2),
        "shipping_fee": round(random.uniform(3, 10), 2),
        "payment_method": random.choice(["credit_card", "PayPal", "ApplePay"]),
        "payment_status": "completed",
        "transaction_date": datetime.utcnow() - timedelta(days=random.randint(0, 180)),
        "billing_address": {
            "name": "John Doe",
            "street": "123 Example St",
            "city": "CityX",
            "state": "StateY",
            "zip": "00000",
            "country": "CountryZ"
        },
        "shipping_address": {
            "name": "John Doe",
            "street": "123 Example St",
            "city": "CityX",
            "state": "StateY",
            "zip": "00000",
            "country": "CountryZ"
        },
        "submission_date": datetime.utcnow()
    }
    order["total"] = round(order["subtotal"] + order["tax"] + order["shipping_fee"], 2)
    orders.append(order)

orders_collection.insert_many(orders)
print(f"Inserted {NUM_ORDERS} fake orders.")