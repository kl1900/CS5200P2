from src.extensions import mongo

def find_all_carts():
    return list(mongo.db.carts.find())

def find_cart_by_id(cart_id):
    return mongo.db.carts.find_one({"cart_id": cart_id})

def create_cart(data):
    return mongo.db.carts.insert_one(data)

def update_cart(cart_id, data):
    return mongo.db.carts.update_one({"cart_id": cart_id}, {"$set": data})

def delete_cart(cart_id):
    return mongo.db.carts.delete_one({"cart_id": cart_id})
