from flask import Blueprint, jsonify
from src.extensions import mongo
from datetime import datetime, timedelta

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/top-products", methods=["GET"])
def top_products():
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.product_id",
            "totalSold": {"$sum": "$items.quantity"}
        }},
        {"$sort": {"totalSold": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "products",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "product"
        }},
        {"$unwind": "$product"},
        {"$project": {
            "_id": 0,
            "productName": "$product.name",
            "totalSold": 1
        }}
    ]
    result = list(mongo.db.orders.aggregate(pipeline))
    return jsonify(result)

@analytics_bp.route("/analytics/most-active-buyers", methods=["GET"])
def most_active_buyers():
    pipeline = [
        {"$group": {
            "_id": "$user_id",
            "totalOrders": {"$sum": 1}
        }},
        {"$sort": {"totalOrders": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "user_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {
            "_id": 0,
            "buyerName": "$user.name",
            "totalOrders": 1
        }}
    ]
    result = list(mongo.db.orders.aggregate(pipeline))
    return jsonify(result)

@analytics_bp.route("/analytics/revenue-by-seller", methods=["GET"])
def revenue_by_seller():
    pipeline = [
        {"$unwind": "$items"},
        {"$lookup": {
            "from": "products",
            "localField": "items.product_id",
            "foreignField": "product_id",
            "as": "product"
        }},
        {"$unwind": "$product"},
        {"$group": {
            "_id": "$product.seller_id",
            "totalRevenue": {
                "$sum": {"$multiply": ["$items.quantity", "$product.price"]}
            }
        }},
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "user_id",
            "as": "seller"
        }},
        {"$unwind": "$seller"},
        {"$project": {
            "_id": 0,
            "sellerName": "$seller.name",
            "totalRevenue": 1
        }},
        {"$sort": {"totalRevenue": -1}}
    ]
    result = list(mongo.db.orders.aggregate(pipeline))
    return jsonify(result)

@analytics_bp.route("/analytics/most-carted-products", methods=["GET"])
def most_carted_products():
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.product_id",
            "cartCount": {"$sum": 1}
        }},
        {"$sort": {"cartCount": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "products",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "product"
        }},
        {"$unwind": "$product"},
        {"$project": {
            "_id": 0,
            "productName": "$product.name",
            "cartCount": 1
        }}
    ]
    result = list(mongo.db.carts.aggregate(pipeline))
    return jsonify(result)

@analytics_bp.route("/analytics/orders-last-7-days", methods=["GET"])
def orders_last_7_days():
    now = datetime.utcnow()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seven_days_ago = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
    pipeline = [
        {"$match": {"transaction_date": {"$gte": seven_days_ago, "$lt": start_of_today}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$transaction_date"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    result = list(mongo.db.orders.aggregate(pipeline))
    return jsonify(result)
