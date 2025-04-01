from flask import Blueprint, jsonify, request

from src.models.user_model import (
    create_user,
    delete_user,
    find_all_users,
    find_user_by_id,
    update_user,
)
from src.utils import serialize_id

user_bp = Blueprint("users", __name__)


@user_bp.route("/", methods=["GET"])
def get_users():
    users = find_all_users()
    return jsonify([serialize_id(user) for user in users]), 200


@user_bp.route("/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(serialize_id(user)), 200
    return jsonify({"error": "User not found"}), 404


@user_bp.route("/", methods=["POST"])
def create_user_route():
    data = request.json
    if find_user_by_id(data.get("user_id")):
        return jsonify({"error": "User ID already exists"}), 400
    create_user(data)
    return jsonify({"message": "User created"}), 201


@user_bp.route("/<string:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.json
    result = update_user(user_id, data)
    if result.matched_count:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404


@user_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    result = delete_user(user_id)
    if result.deleted_count:
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404
