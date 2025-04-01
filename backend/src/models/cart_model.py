from src.extensions import mongo
from src.utils import clean_mongo_result


@clean_mongo_result
def find_all_carts():
    return list(mongo.db.carts.find())


@clean_mongo_result
def find_cart_by_id(cart_id):
    return mongo.db.carts.find_one({"cart_id": cart_id})


@clean_mongo_result
def create_cart(data):
    return mongo.db.carts.insert_one(data)


@clean_mongo_result
def update_cart(cart_id, data):
    return mongo.db.carts.update_one({"cart_id": cart_id}, {"$set": data})


@clean_mongo_result
def delete_cart(cart_id):
    return mongo.db.carts.delete_one({"cart_id": cart_id})
