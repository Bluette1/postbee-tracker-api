from datetime import datetime
from flask import Blueprint, jsonify, request
from app.utils.auth import token_required
from app.models.job_interaction import JobInteraction
import requests
from app.config import get_config

config = get_config()

job_interaction_routes = Blueprint("job_interaction_routes", __name__)

RAILS_API_URL = config.RAILS_API_URL

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


@job_interaction_routes.route('/<string:job_id>/view', methods=['POST'])
def track_view(job_id):
    try:
        response = requests.post(f"{RAILS_API_URL}/job_posts/{job_id}/increment_view_count")
        response.raise_for_status()
        data = response.json()
        view_count = data.get('view_count')
        last_viewed = data.get('last_viewed') 
    except requests.exceptions.RequestException as e:
        print("Error updating view count in Rails API:", e)
        return {"error": "Failed to update view count"}, 500

    return {
        "message": "View tracked successfully",
        "view_count": view_count,
        "last_viewed": last_viewed
    }, 200

@job_interaction_routes.route('/<string:job_id>/interaction', methods=['POST'])
@token_required
def track_interaction(job_id):
    user_id = request.user.get("user_id")

    interaction = JobInteraction.find(user_id, job_id)
    
    if not interaction:
        new_interaction = JobInteraction(user_id=user_id, job_id=job_id)
        new_interaction.save()

    return {
        "message": "Interaction tracked successfully"
    }, 200

@job_interaction_routes.route('/status/<string:job_id>', methods=['GET'])
@token_required
def get_interaction_status(job_id):
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    try:
        response = requests.get(f"{RAILS_API_URL}/job_posts/{job_id}")
        response.raise_for_status()
        job_post_data = response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching job post from Rails API:", e)
        return jsonify({"error": "Failed to fetch job post"}), 500

    if job_post_data:
        response = {
            "isPinned": interaction.is_pinned if interaction else False,
            "isSaved": interaction.is_saved if interaction else False,
            "hasFollowUp": interaction.has_follow_up if interaction else False,
            "viewCount": job_post_data.get('view_count', 0),  
            "lastViewed": job_post_data.get('last_viewed'),
        }
    else:
        # If no job post exists, return default values
        response = {
            "isPinned": False,
            "isSaved": False,
            "hasFollowUp": False,
            "viewCount": 0,
            "lastViewed": None,
        }

    return jsonify(response), 200

