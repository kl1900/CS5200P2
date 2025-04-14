from flask import Blueprint, jsonify, request

from src.models.cart_model import *

from src.jwt_utils import role_required  # Import the decorator

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


# Add: "Get My Cart" Route
@cart_bp.route("/me", methods=["GET"])
@role_required("make_purchase")
def get_my_cart():
    user_id = request.current_user["user_id"]
    cart = find_cart_by_user_id(user_id)

    if not cart:
        return jsonify({"message": "Cart is empty", "items": []}), 200
    return jsonify(cart), 200


# Add: "Add to Cart" Route
@cart_bp.route("/add", methods=["POST"])
@role_required("make_purchase")
def add_to_cart():
    user_id = request.current_user["user_id"]
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    cart = find_cart_by_user_id(user_id)
    if not cart:
        cart = {"user_id": user_id, "items": []}

    # Check if item already in cart
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        cart["items"].append({"product_id": product_id, "quantity": quantity})

    update_cart_by_user_id(user_id, cart["items"])
    return jsonify({"message": "Product added to cart"}), 200

