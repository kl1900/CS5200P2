from src.db import get_db
from src.utils import clean_mongo_result


@clean_mongo_result
def find_all_carts():
    return list(get_db().carts.find())

@clean_mongo_result
def find_cart_by_user_id(cart_id):
    return get_db().carts.find({"user_id": cart_id})

@clean_mongo_result
def find_cart_by_cart_id(cart_id):
    return get_db().carts.find_one({"cart_id": cart_id})


@clean_mongo_result
def create_cart(data):
    return get_db().carts.insert_one(data)


@clean_mongo_result
def update_cart(cart_id, data):
    return get_db().carts.update_one({"cart_id": cart_id}, {"$set": data})


@clean_mongo_result
def delete_cart(cart_id):
    return get_db().carts.delete_one({"cart_id": cart_id})
