from src.extensions import mongo

def find_all_products():
    return list(mongo.db.products.find())

def find_product_by_id(product_id):
    return mongo.db.products.find_one({"product_id": product_id})

def create_product(data):
    return mongo.db.products.insert_one(data)

def update_product(product_id, data):
    return mongo.db.products.update_one({"product_id": product_id}, {"$set": data})

def delete_product(product_id):
    return mongo.db.products.delete_one({"product_id": product_id})
