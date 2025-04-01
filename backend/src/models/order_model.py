from src.extensions import mongo


def find_all_orders():
    return list(mongo.db.orders.find())


def find_order_by_id(order_id):
    return mongo.db.orders.find_one({"order_id": order_id})


def create_order(data):
    return mongo.db.orders.insert_one(data)


def update_order(order_id, data):
    return mongo.db.orders.update_one({"order_id": order_id}, {"$set": data})


def delete_order(order_id):
    return mongo.db.orders.delete_one({"order_id": order_id})
