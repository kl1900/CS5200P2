"checkout route"
from datetime import datetime

from bson import ObjectId
from flask import Blueprint, jsonify, request

from src.extensions import mongo

checkout_bp = Blueprint("checkout", __name__)

# Expexted checkout request body
# {
#   "user_id": "user_001",
#   "cart_id": "cart_00089",
#   "payment_method": "credit_card",
#   "billing_address": {
#     "name": "Foo bar",
#     "street": "example Lane",
#     "city": "Vancouver",
#     "state": "BC",
#     "zip": "",
#     "country": "Canada"
#   },
#   "shipping_address": {
#     "name": "Foo Bar",
#     "street": "example Lane",
#     "city": "Vancouver",
#     "state": "BC",
#     "zip": "",
#     "country": "Canada"
#   }
# }


@checkout_bp.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    user_id = data.get("user_id")
    cart_id = data.get("cart_id")

    if not user_id or not cart_id:
        return jsonify({"error": "Missing user_id or cart_id"}), 400
    
    billing_address = data.get("billing_address", {})
    shipping_address = data.get("shipping_address", {})
    payment_method = data.get("payment_method", "credit_card")

    client = mongo.cx

    with client.start_session() as session:

        def txn_ops(s):
            cart = mongo.db.cart.find_one(
                {"user_id": user_id, "cart_id": cart_id, "status": "active"}, session=s
            )
            if not cart:
                raise Exception("No active cart found.")
            
            now = datetime.utcnow().isoformat() + "Z"

            # Compute order totals
            order_items = []
            subtotal = 0.0

            for item in cart["items"]:
                item_subtotal = item["price"] * item["quantity"]
                subtotal += item_subtotal

                order_items.append({
                    "product_id": item["product_id"],
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "unit_price": item["price"],
                    "subtotal": item_subtotal
                })

            tax = round(subtotal * 0.1, 2)  # e.g. 10% tax
            shipping_fee = 5.00  # fixed
            total = subtotal + tax + shipping_fee

            # Insert order
            mongo.db.orders.insert_one({
                "user_id": user_id,
                "order_id": f"order_{str(ObjectId())[-5:]}",  # quick unique suffix
                "items": order_items,
                "subtotal": subtotal,
                "tax": tax,
                "shipping_fee": shipping_fee,
                "total": total,
                "payment_method": payment_method,
                "payment_status": "completed",
                "transaction_date": now,
                "submission_date": now,
                "billing_address": billing_address,
                "shipping_address": shipping_address
            }, session=s)

            # Mark cart as checked_out
            mongo.db.cart.update_one(
                {"_id": cart["_id"]}, {"$set": {"status": "checked_out"}}, session=s
            )

            # Create new active cart
            mongo.db.cart.insert_one(
                {
                    "user_id": user_id,
                    "cart_id": str(ObjectId()),  # New cart ID
                    "status": "active",
                    "items": [],
                },
                session=s,
            )

        try:
            session.with_transaction(txn_ops)
            return jsonify({"message": "Checkout successful"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
