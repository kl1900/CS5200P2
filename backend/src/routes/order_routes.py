from flask import Blueprint, request, jsonify
from src.models.order_model import *
from src.utils import serialize_id

order_bp = Blueprint("orders", __name__)

@order_bp.route("/", methods=["GET"])
def get_orders():
    return jsonify([serialize_id(order) for order in find_all_orders()]), 200

@order_bp.route("/<string:order_id>", methods=["GET"])
def get_order(order_id):
    order = find_order_by_id(order_id)
    if order:
        return jsonify(serialize_id(order)), 200
    return jsonify({"error": "Order not found"}), 404

@order_bp.route("/", methods=["POST"])
def create_order_route():
    data = request.json
    if find_order_by_id(data.get("order_id")):
        return jsonify({"error": "Order ID already exists"}), 400
    create_order(data)
    return jsonify({"message": "Order created"}), 201

@order_bp.route("/<string:order_id>", methods=["PUT"])
def update_order_route(order_id):
    data = request.json
    result = update_order(order_id, data)
    if result.matched_count:
        return jsonify({"message": "Order updated"}), 200
    return jsonify({"error": "Order not found"}), 404

@order_bp.route("/<string:order_id>", methods=["DELETE"])
def delete_order_route(order_id):
    result = delete_order(order_id)
    if result.deleted_count:
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"error": "Order not found"}), 404
