from flask import Blueprint, jsonify, request

from src.models.order_model import *

from src.jwt_utils import role_required  # decorator
order_bp = Blueprint("orders", __name__)


@order_bp.route("/", methods=["GET"])
@role_required("make_purchase")
def get_orders():
    user_id = request.current_user["user_id"]
    return jsonify(find_all_orders(user_id)), 200


@order_bp.route("/<string:order_id>", methods=["GET"])
@role_required("make_purchase")
def get_order(order_id):
    order = find_order_by_id(order_id)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404


@order_bp.route("/", methods=["POST"])
@role_required("make_purchase")
def create_order_route():
    data = request.json
    if find_order_by_id(data.get("order_id")):
        return jsonify({"error": "Order ID already exists"}), 400
    create_order(data)
    return jsonify({"message": "Order created"}), 201


@order_bp.route("/<string:order_id>", methods=["PUT"])
@role_required("make_purchase")
def update_order_route(order_id):
    data = request.json
    result = update_order(order_id, data)
    if result.matched_count:
        return jsonify({"message": "Order updated"}), 200
    return jsonify({"error": "Order not found"}), 404


@order_bp.route("/<string:order_id>", methods=["DELETE"])
@role_required("make_purchase")
def delete_order_route(order_id):
    result = delete_order(order_id)
    if result.deleted_count:
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"error": "Order not found"}), 404


