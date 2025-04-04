from src.extensions import mongo
from src.utils import clean_mongo_result


@clean_mongo_result
def find_all_users():
    return list(mongo.db.users.find())


@clean_mongo_result
def find_user_by_id(user_id):
    return mongo.db.users.find_one({"user_id": user_id})


@clean_mongo_result
def create_user(data):
    return mongo.db.users.insert_one(data)


@clean_mongo_result
def update_user(user_id, data):
    return mongo.db.users.update_one({"user_id": user_id}, {"$set": data})


@clean_mongo_result
def delete_user(user_id):
    return mongo.db.users.delete_one({"user_id": user_id})


@clean_mongo_result
def find_user_by_email(email):
    return mongo.db.users.find_one({"email": email})
