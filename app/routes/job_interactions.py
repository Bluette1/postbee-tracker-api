from datetime import datetime
from flask import Blueprint, jsonify, request
from app.utils.auth import token_required
from app.models.job_interaction import JobInteraction

job_interaction_routes = Blueprint("job_interaction_routes", __name__)


@job_interaction_routes.route("/<string:job_id>/pin", methods=["POST"])
@token_required
def toggle_pin(job_id: str) -> tuple:
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if interaction:
        interaction.is_pinned = not interaction.is_pinned
        interaction.update() 
    else:
        interaction = JobInteraction(user_id=user_id, job_id=job_id, is_pinned=True)
        interaction.save()

    return jsonify({"isPinned": interaction.is_pinned}), 200


@job_interaction_routes.route("/<string:job_id>/save", methods=["POST"])
@token_required
def toggle_save(job_id: str) -> tuple:
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if interaction:
        interaction.is_saved = not interaction.is_saved
        interaction.update()
    else:
        interaction = JobInteraction(user_id=user_id, job_id=job_id, is_saved=True)
        interaction.save()

    return jsonify({"isSaved": interaction.is_saved}), 200


@job_interaction_routes.route("/<string:job_id>/follow-ups", methods=["POST"])
@token_required
def create_follow_up(job_id: str) -> tuple:
    user_id = request.user.get("user_id")
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    interaction = JobInteraction.find(user_id, job_id)

    if not interaction:
        interaction = JobInteraction(
            user_id=user_id, job_id=job_id, follow_up_data=data, has_follow_up=True
        )
        interaction.save()
    else:
        interaction.follow_up_data = data
        interaction.has_follow_up = True
        interaction.update()

    return jsonify(data), 200


@job_interaction_routes.route(
    "/<string:job_id>/follow-ups/<int:follow_up_id>", methods=["PUT"]
)
@token_required
def update_follow_up(job_id: str, follow_up_id: int) -> tuple:
    user_id = request.user.get("user_id")
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    interaction = JobInteraction.find(user_id, job_id)

    if not interaction:
        return jsonify({"message": "Follow-up not found"}), 404

    interaction.follow_up_data = data
    interaction.update()

    return jsonify(data), 200


@job_interaction_routes.route("/<string:job_id>/follow-ups", methods=["GET"])
@token_required
def get_follow_up(job_id: str) -> tuple:
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if not interaction or not interaction.follow_up_data:
        return jsonify({"message": "Follow-up not found"}), 404

    return jsonify(interaction.follow_up_data), 200


@job_interaction_routes.route("/<string:job_id>/view", methods=["POST"])
@token_required
def track_view(job_id: str) -> tuple:
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if interaction:
        interaction.view_count += 1
        interaction.last_viewed = datetime.utcnow()
        interaction.update()
    else:
        interaction = JobInteraction(
            user_id=user_id, job_id=job_id, view_count=1, last_viewed=datetime.utcnow()
        )
        interaction.save()

    return jsonify({}), 200
