from flask import Blueprint, jsonify, request

from webapp.utils.auth import token_required

tracking_routes = Blueprint("tracking_routes", __name__)


@tracking_routes.route("/tracking/", methods=["POST"])
@token_required
def track_interaction():
    user_id = request.user.get("user_id")
    return jsonify({"message": "User tracked successfully", "user_id": user_id}), 201


@tracking_routes.route("/tracking/<int:tracking_id>", methods=["GET"])
@token_required
def get_tracking(tracking_id):
    user_id = request.user.get("user_id")
    return jsonify(
        {"message": f"Tracking detail for ID {tracking_id}", "user_id": user_id}
    )
