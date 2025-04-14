from src.db import get_db
from src.utils import clean_mongo_result


@clean_mongo_result
def find_all_orders():
    return list(get_db().orders.find())


@clean_mongo_result
def find_order_by_id(order_id):
    return get_db().orders.find_one({"order_id": order_id})


@clean_mongo_result
def create_order(data):
    return get_db().orders.insert_one(data)


@clean_mongo_result
def update_order(order_id, data):
    return get_db().orders.update_one({"order_id": order_id}, {"$set": data})


@clean_mongo_result
def delete_order(order_id):
    return get_db().orders.delete_one({"order_id": order_id})
