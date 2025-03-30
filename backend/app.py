from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/mydb')
client = MongoClient(mongo_uri)
db = client.get_database()

@app.route('/')
def index():
    return jsonify({"message": "Flask backend is running!"})

@app.route('/items', methods=['GET'])
def get_items():
    items = list(db.items.find({}, {'_id': 0}))
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    db.items.insert_one(data)
    return jsonify({"message": "Item added!"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
