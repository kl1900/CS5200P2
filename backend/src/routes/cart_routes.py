from flask import Blueprint, request, jsonify
from src.models.cart_model import *
from src.utils import serialize_id

cart_bp = Blueprint("carts", __name__)

@cart_bp.route("/", methods=["GET"])
def get_carts():
    return jsonify([serialize_id(cart) for cart in find_all_carts()]), 200

@cart_bp.route("/<string:cart_id>", methods=["GET"])
def get_cart(cart_id):
    cart = find_cart_by_id(cart_id)
    if cart:
        return jsonify(serialize_id(cart)), 200
    return jsonify({"error": "Cart not found"}), 404

@cart_bp.route("/", methods=["POST"])
def create_cart_route():
    data = request.json
    if find_cart_by_id(data.get("cart_id")):
        return jsonify({"error": "Cart ID already exists"}), 400
    create_cart(data)
    return jsonify({"message": "Cart created"}), 201

@cart_bp.route("/<string:cart_id>", methods=["PUT"])
def update_cart_route(cart_id):
    data = request.json
    result = update_cart(cart_id, data)
    if result.matched_count:
        return jsonify({"message": "Cart updated"}), 200
    return jsonify({"error": "Cart not found"}), 404

@cart_bp.route("/<string:cart_id>", methods=["DELETE"])
def delete_cart_route(cart_id):
    result = delete_cart(cart_id)
    if result.deleted_count:
        return jsonify({"message": "Cart deleted"}), 200
    return jsonify({"error": "Cart not found"}), 404
