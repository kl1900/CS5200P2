"checkout route"
from datetime import datetime

from bson import ObjectId
from flask import Blueprint, jsonify, request

from src.db import get_db, get_client

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

def txn_ops_factory(user_id, cart_id, data, db):
    def txn_ops(session):
        billing_address = data.get("billing_address", {})
        shipping_address = data.get("shipping_address", {})
        payment_method = data.get("payment_method", "credit_card")
        cart = get_db().cart.find_one(
                {"user_id": user_id, "cart_id": cart_id, "status": "active"}, session=session
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
        db.orders.insert_one({
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
        }, session=session)

        # Mark cart as checked_out
        db.cart.update_one(
            {"_id": cart["_id"]}, {"$set": {"status": "checked_out"}}, session=session
        )

        # Create new active cart
        db.cart.insert_one(
            {
                "user_id": user_id,
                "cart_id": str(ObjectId()),  # New cart ID
                "status": "active",
                "items": [],
            },
            session=session,
        )
    return txn_ops


@checkout_bp.route("/api/checkout", methods=["POST"])
def checkout():
    db = get_db()
    data = request.get_json()
    user_id = data.get("user_id")
    cart_id = data.get("cart_id")

    if not user_id or not cart_id:
        return jsonify({"error": "Missing user_id or cart_id"}), 400

    with get_client().start_session() as session:
        try:
            txn_ops = txn_ops_factory(user_id, cart_id, data, db)
            session.with_transaction(txn_ops)
            return jsonify({"message": "Checkout successful"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
