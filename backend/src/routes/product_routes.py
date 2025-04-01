from flask import Blueprint, request, jsonify
from src.models.product_model import *
from src.utils import serialize_id

product_bp = Blueprint("products", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    return jsonify([serialize_id(p) for p in find_all_products()]), 200

@product_bp.route("/<string:product_id>", methods=["GET"])
def get_product(product_id):
    product = find_product_by_id(product_id)
    if product:
        return jsonify(serialize_id(product)), 200
    return jsonify({"error": "Product not found"}), 404

@product_bp.route("/", methods=["POST"])
def create_product_route():
    data = request.json
    if find_product_by_id(data.get("product_id")):
        return jsonify({"error": "Product ID already exists"}), 400
    create_product(data)
    return jsonify({"message": "Product created"}), 201

@product_bp.route("/<string:product_id>", methods=["PUT"])
def update_product_route(product_id):
    data = request.json
    result = update_product(product_id, data)
    if result.matched_count:
        return jsonify({"message": "Product updated"}), 200
    return jsonify({"error": "Product not found"}), 404

@product_bp.route("/<string:product_id>", methods=["DELETE"])
def delete_product_route(product_id):
    result = delete_product(product_id)
    if result.deleted_count:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404
