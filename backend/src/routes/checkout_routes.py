# routes.py or inside your Flask app

from flask import Blueprint, request, jsonify
from bson import ObjectId
from src.extensions import mongo, db

checkout_bp = Blueprint("checkout", __name__)

@checkout_bp.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    user_id = data.get("user_id")
    cart_id = data.get("cart_id")

    if not user_id or not cart_id:
        return jsonify({"error": "Missing user_id or cart_id"}), 400

    client = mongo.cx

    with client.start_session() as session:
        def txn_ops(s):
            cart = db.cart.find_one(
                {"user_id": user_id, "cart_id": cart_id, "status": "active"},
                session=s
            )
            if not cart:
                raise Exception("No active cart found.")

            # Deduct inventory
            for item in cart["items"]:
                result = db.inventory.update_one(
                    {"product_id": item["product_id"], "stock": {"$gte": item["quantity"]}},
                    {"$inc": {"stock": -item["quantity"]}},
                    session=s
                )
                if result.modified_count == 0:
                    raise Exception(f"Insufficient stock for {item['product_id']}")

            # Create order
            db.orders.insert_one({
                "user_id": user_id,
                "items": cart["items"],
                "total": sum(item["price"] * item["quantity"] for item in cart["items"]),
                "status": "confirmed"
            }, session=s)

            # Mark cart as checked_out
            db.cart.update_one(
                {"_id": cart["_id"]},
                {"$set": {"status": "checked_out"}},
                session=s
            )

            # Create new active cart
            db.cart.insert_one({
                "user_id": user_id,
                "cart_id": str(ObjectId()),  # New cart ID
                "status": "active",
                "items": []
            }, session=s)

        try:
            session.with_transaction(txn_ops)
            return jsonify({"message": "Checkout successful"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
