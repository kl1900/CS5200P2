from src.extensions import mongo

def find_all_users():
    return list(mongo.db.users.find())

def find_user_by_id(user_id):
    return mongo.db.users.find_one({"user_id": user_id})

def create_user(data):
    return mongo.db.users.insert_one(data)

def update_user(user_id, data):
    return mongo.db.users.update_one({"user_id": user_id}, {"$set": data})

def delete_user(user_id):
    return mongo.db.users.delete_one({"user_id": user_id})
