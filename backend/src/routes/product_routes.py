from dataclasses import asdict
from flask import Blueprint, jsonify, request

from src.models.product_model import *

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
def get_products():
    return jsonify([asdict(p) for p in find_all_products()]), 200


@product_bp.route("/<string:product_id>", methods=["GET"])
def get_product(product_id):
    product = find_product_by_id(product_id)
    if product:
        return jsonify(asdict(product)), 200
    return jsonify({"error": "Product not found"}), 404


@product_bp.route("/", methods=["POST"])
def create_product_route():
    data = request.json
    try:
        # Check if product_id already exists
        if "product_id" in data and find_product_by_id(data.get("product_id")):
            return jsonify({"error": "Product ID already exists"}), 400
        
        # Create the product
        new_product = create_product(data)
        if new_product:
            return jsonify(asdict(new_product)), 201
        return jsonify({"error": "Failed to create product"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@product_bp.route("/<string:product_id>", methods=["PUT"])
def update_product_route(product_id):
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    result = update_product(product_id, data)
    
    if result.matched_count:
        # Get the updated product to return
        updated_product = find_product_by_id(product_id)
        if updated_product:
            return jsonify(asdict(updated_product)), 200
        return jsonify({"message": "Product updated"}), 200
    
    return jsonify({"error": "Product not found"}), 404


@product_bp.route("/<string:product_id>", methods=["DELETE"])
def delete_product_route(product_id):
    # TODO: remove all related data in carts
    result = delete_product(product_id)
    if result.deleted_count:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404