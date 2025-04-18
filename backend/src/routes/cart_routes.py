from flask import Blueprint, jsonify, request

from src.models.cart_model import *

from src.models.product_model import find_product_by_id

from src.models.order_model import create_order

from src.jwt_utils import role_required  # Import the decorator

from datetime import datetime

import uuid

cart_bp = Blueprint("carts", __name__)


@cart_bp.route("/<string:cart_id>", methods=["GET"])
@role_required("make_purchase")
def get_cart(cart_id):
    cart = find_cart_by_cart_id(cart_id)
    if cart:
        return jsonify(cart), 200
    return jsonify({"error": "Cart not found"}), 404


@cart_bp.route("/", methods=["POST"])
@role_required("make_purchase")
def create_cart_route():
    data = request.json
    if find_cart_by_cart_id(data.get("cart_id")):
        return jsonify({"error": "Cart ID already exists"}), 400
    create_cart(data)
    return jsonify({"message": "Cart created"}), 201


@cart_bp.route("/<string:cart_id>", methods=["PUT"])
@role_required("make_purchase")
def update_cart_route(cart_id):
    data = request.json
    result = update_cart(cart_id, data)
    if result.matched_count:
        return jsonify({"message": "Cart updated"}), 200
    return jsonify({"error": "Cart not found"}), 404


@cart_bp.route("/<string:cart_id>", methods=["DELETE"])
@role_required("make_purchase")
def delete_cart_route(cart_id):
    result = delete_cart(cart_id)
    if result.deleted_count:
        return jsonify({"message": "Cart deleted"}), 200
    return jsonify({"error": "Cart not found"}), 404


# "Get My Cart" Route
@cart_bp.route("/me", methods=["GET"])
@role_required("make_purchase")
def get_my_cart():
    user_id = request.current_user["user_id"]
    cart = find_cart_by_user_id(user_id)

    if not cart:
        return jsonify({"message": "Cart is empty", "items": []}), 200
    return jsonify(cart), 200


# "Add to Cart" Route
@cart_bp.route("/add", methods=["POST"])
@role_required("make_purchase")
def add_to_cart():
    user_id = request.current_user["user_id"]
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    product = find_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart = find_cart_by_user_id(user_id)
    if not cart:
        # If no cart, create a new one with a unique cart_id
        new_cart = {
            "cart_id": f"cart_{user_id}",
            "user_id": user_id,
            "items": [{
                "product_id": product.product_id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity
            }],
            "status": "active"
        }
        create_cart(new_cart)
        return jsonify({"message": "New cart created and product added"}), 201

    # Modify existing cart
    found = False
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            found = True
            break

    if not found:
        cart["items"].append({
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity
        })

    update_cart(cart["cart_id"], {"items": cart["items"]})
    return jsonify({"message": "Product added to existing cart"}), 200


# "Remove an Item from Cart" Route
@cart_bp.route("/remove", methods=["POST"])
@role_required("make_purchase")
def remove_from_cart():
    user_id = request.current_user["user_id"]
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    cart = find_cart_by_user_id(user_id)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    updated_items = [item for item in cart.get("items", []) if item["product_id"] != product_id]
    update_cart_by_user_id(user_id, updated_items)

    return jsonify({"message": "Item removed from cart"}), 200


# "Cart Checkout" Route
@cart_bp.route("/checkout", methods=["POST"])
@role_required("make_purchase")
def checkout():
    user = request.current_user
    user_id = user["user_id"]
    data = request.get_json()

    # Get cart
    cart = find_cart_by_user_id(user_id)
    if not cart or not cart.get("items"):
        return jsonify({"error": "Cart is empty"}), 400

    items = cart["items"]
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = round(subtotal * 0.1, 2)
    shipping_fee = 5.00
    total = subtotal + tax + shipping_fee

    order_data = {
        "order_id": f"order_{str(uuid.uuid4())[:8]}",
        "user_id": user_id,
        "items": [
            {
                "product_id": item["product_id"],
                "name": item.get("name", ""),
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "subtotal": item["quantity"] * item["price"]
            } for item in items
        ],
        "subtotal": subtotal,
        "tax": tax,
        "shipping_fee": shipping_fee,
        "total": total,
        "payment_method": data.get("payment_method", "credit_card"),
        "payment_status": "completed",
        "transaction_date": datetime.utcnow().isoformat(),
        "billing_address": data.get("billing_address"),
        "shipping_address": data.get("shipping_address"),
        "submission_date": datetime.utcnow().isoformat()
    }

    # Save order and empty cart
    create_order(order_data)
    update_cart_by_user_id(user_id, [])

    # Remove MongoDB-specific ObjectId before returning
    order_data.pop("_id", None)

    return jsonify({"message": "Checkout successful", "order": order_data}), 200