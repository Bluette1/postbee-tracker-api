from flask import Blueprint, jsonify, request

from app.utils.auth import validate_token

tracking_routes = Blueprint("tracking_routes", __name__)


@tracking_routes.route("/trackings", methods=["POST"])
@validate_token
def track_interaction():
    user_id = request.user.get("user_id")
    return jsonify({"message": "User tracked successfully", "user_id": user_id}), 201


@tracking_routes.route("/trackings/<int:tracking_id>", methods=["GET"])
@validate_token
def get_tracking(tracking_id):
    user_id = request.user.get("user_id")
    return jsonify(
        {"message": f"Tracking detail for ID {tracking_id}", "user_id": user_id}
    )
