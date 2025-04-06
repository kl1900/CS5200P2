from flask import Blueprint, jsonify, request

from src.models.cart_model import *

from src.jwt_utils import role_required  # Import the decorator

cart_bp = Blueprint("carts", __name__)


@cart_bp.route("/", methods=["GET"])
@role_required("make_purchase")
def get_carts():
    return jsonify(find_all_carts()), 200


@cart_bp.route("/<string:cart_id>", methods=["GET"])
@role_required("make_purchase")
def get_cart(cart_id):
    cart = find_cart_by_id(cart_id)
    if cart:
        return jsonify(cart), 200
    return jsonify({"error": "Cart not found"}), 404


@cart_bp.route("/", methods=["POST"])
@role_required("make_purchase")
def create_cart_route():
    data = request.json
    if find_cart_by_id(data.get("cart_id")):
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
