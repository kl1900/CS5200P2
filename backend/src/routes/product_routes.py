from dataclasses import asdict

from flask import Blueprint, jsonify, request

from src.models.product_model import *

from src.jwt_utils import role_required

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
@role_required("view_products")
def get_products():
    current_user = request.current_user
    products = find_all_products(current_user=current_user)
    return jsonify([asdict(p) for p in products]), 200


@product_bp.route("/<string:product_id>", methods=["GET"])
@role_required("view_products")
def get_product(product_id):
    product = find_product_by_id(product_id)
    if product:
        return jsonify(asdict(product)), 200
    return jsonify({"error": "Product not found"}), 404


@product_bp.route("/", methods=["POST"])
@role_required("view_products") # used for testing purpose. Admin can list product with this setup
def create_product_route():
    data = request.json
    if find_product_by_id(data.get("product_id")):
        return jsonify({"error": "Product ID already exists"}), 400
    new_product = create_product(data)
    if new_product:
        return jsonify({"message": "Product created"}), 201
    return jsonify({"message": "failed to create product"}), 400


@product_bp.route("/<string:product_id>", methods=["PUT"])
@role_required("edit_product")
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
@role_required("delete_product")
def delete_product_route(product_id):
    # TODO: remove all related data in carts
    result = delete_product(product_id)
    if result.deleted_count:
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404
