from dataclasses import asdict

from flask import Blueprint, jsonify, request

from src.models.product_model import *
from src.utils import serialize_id

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
    if find_product_by_id(data.get("product_id")):
        return jsonify({"error": "Product ID already exists"}), 400
    new_product = create_product(data)
    if new_product:
        return jsonify({"message": "Product created"}), 201
    return jsonify({"message": "failed to create product"}), 400


@product_bp.route("/<string:product_id>", methods=["PUT"])
def update_product_route(product_id):
    data = request.get_json(force=True, silent=True)
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
