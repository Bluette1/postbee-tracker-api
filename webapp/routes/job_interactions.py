from datetime import datetime, timezone

import requests
from dateutil import parser
from flask import Blueprint, current_app, jsonify, request

from webapp.config import get_config
from webapp.models.job_interaction import JobInteraction
from webapp.producer import publish_job_application
from webapp.tasks.jobs import send_followup_notification
from webapp.utils.auth import token_required


def get_logger():
    return current_app.logger


config = get_config()
job_interaction_routes = Blueprint("job_interaction_routes", __name__)
RAILS_API_URL = config.RAILS_API_URL


@job_interaction_routes.route("/<string:job_id>/pin", methods=["POST"])
@token_required
def toggle_pin(job_id: str) -> tuple:
    logger = get_logger()
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if interaction:
        interaction.is_pinned = not interaction.is_pinned
        interaction.update()
        logger.info(
            "Toggled pin for job_id: %s by user_id: %s to %s",
            job_id,
            user_id,
            interaction.is_pinned,
        )
    else:
        interaction = JobInteraction(user_id=user_id, job_id=job_id, is_pinned=True)
        interaction.save()
        logger.info("Pinned job_id: %s by user_id: %s", job_id, user_id)

    return jsonify({"isPinned": interaction.is_pinned}), 200


@job_interaction_routes.route("/<string:job_id>/save", methods=["POST"])
@token_required
def toggle_save(job_id: str) -> tuple:
    logger = get_logger()
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if interaction:
        interaction.is_saved = not interaction.is_saved
        interaction.update()
        logger.info(
            "Toggled save for job_id: %s by user_id: %s to %s",
            job_id,
            user_id,
            interaction.is_saved,
        )
    else:
        interaction = JobInteraction(user_id=user_id, job_id=job_id, is_saved=True)
        interaction.save()
        logger.info("Saved job_id: %s by user_id: %s", job_id, user_id)

    return jsonify({"isSaved": interaction.is_saved}), 200


@job_interaction_routes.route("/<string:job_id>/follow-ups", methods=["POST"])
@token_required
def create_follow_up(job_id: str) -> tuple:
    logger = get_logger()
    user_id = request.user.get("user_id")
    user_email = request.user.get("email")
    data = request.get_json()

    if not data:
        logger.warning(
            "No data provided for follow-up creation by user_id: %s", user_id
        )
        return jsonify({"message": "No data provided"}), 400

    interaction = JobInteraction.find(user_id, job_id)

    if not interaction:
        interaction = JobInteraction(
            user_id=user_id, job_id=job_id, follow_up_data=data, has_follow_up=True
        )
        interaction.save()
        logger.info("Created follow-up for job_id: %s by user_id: %s", job_id, user_id)
    else:
        interaction.follow_up_data = data
        interaction.has_follow_up = True
        interaction.update()
        logger.info("Updated follow-up for job_id: %s by user_id: %s", job_id, user_id)

    data["user_email"] = user_email

    # Use dateutil.parser to parse the followUpDate
    follow_up_date = parser.isoparse(data["followUpDate"])

    # Calculate delay using offset-aware datetime
    delay = (follow_up_date - datetime.now(timezone.utc)).total_seconds()

    if delay > 0:
        # Schedule the task
        send_followup_notification.apply_async(args=[data], eta=follow_up_date)
        logger.info(
            f"Scheduled follow-up notification for job ID: {data['jobId']} at {follow_up_date}."
        )
    else:
        logger.warning("The follow-up date is in the past. Email will not be sent.")

    if data["status"] == "applied":

        publish_job_application(job_id, user_id)
        logger.info(f"Sent job application message for job ID: {data['jobId']}.")
    return jsonify(data), 200


@job_interaction_routes.route("/<string:job_id>/follow-ups", methods=["PUT"])
@token_required
def update_follow_up(job_id: str) -> tuple:
    logger = get_logger()
    user_id = request.user.get("user_id")
    user_email = request.user.get("email")
    data = request.get_json()

    if not data:
        logger.warning("No data provided for follow-up update by user_id: %s", user_id)
        return jsonify({"message": "No data provided"}), 400

    interaction = JobInteraction.find(user_id, job_id)

    if not interaction:
        logger.warning(
            "Follow-up not found for job_id: %s by user_id: %s", job_id, user_id
        )
        return jsonify({"message": "Follow-up not found"}), 404

    interaction.follow_up_data = data
    interaction.update()
    logger.info("Updated follow-up for job_id: %s by user_id: %s", job_id, user_id)

    # Collect follow-up data from the request
    followup_data = {
        "jobId": data["jobId"],
        "status": data["status"],
        "notes": data.get("notes"),
        "nextStep": data.get("nextStep"),
        "followUpDate": data.get("followUpDate"),
        "user_email": user_email,
    }

    # Use dateutil.parser to parse the followUpDate
    follow_up_date = parser.isoparse(data["followUpDate"])

    # Calculate delay using offset-aware datetime
    delay = (follow_up_date - datetime.now(timezone.utc)).total_seconds()

    if delay > 0:
        # Schedule the task
        send_followup_notification.apply_async(args=[followup_data], eta=follow_up_date)
        logger.info(
            f"Scheduled follow-up notification for job ID: {data['jobId']} at {follow_up_date}."
        )
    else:
        logger.warning("The follow-up date is in the past. Email will not be sent.")

    if data["status"] == "applied":
        publish_job_application(job_id, user_id)
        logger.info(f"Sent job application message for job ID: {data['jobId']}.")
    return jsonify(data), 200


@job_interaction_routes.route("/<string:job_id>/follow-ups", methods=["GET"])
@token_required
def get_follow_up(job_id: str) -> tuple:
    logger = get_logger()
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if not interaction or not interaction.follow_up_data:
        logger.warning(
            "Follow-up not found for job_id: %s by user_id: %s", job_id, user_id
        )
        return jsonify({"message": "Follow-up not found"}), 404

    logger.info("Retrieved follow-up for job_id: %s by user_id: %s", job_id, user_id)
    return jsonify(interaction.follow_up_data), 200


@job_interaction_routes.route("/<string:job_id>/view", methods=["POST"])
def track_view(job_id):
    logger = get_logger()
    logger.info("Tracking view for job_id: %s", job_id)
    try:
        response = requests.post(
            f"{RAILS_API_URL}/job_posts/{job_id}/increment_view_count"
        )
        response.raise_for_status()
        data = response.json()
        view_count = data.get("view_count")
        last_viewed = data.get("last_viewed")
        logger.info("Updated view count for job_id: %s to %s", job_id, view_count)
    except requests.exceptions.RequestException as e:
        logger.error(
            "Error updating view count in Rails API for job_id %s: %s", job_id, e
        )
        return {"error": "Failed to update view count"}, 500

    return {
        "message": "View tracked successfully",
        "view_count": view_count,
        "last_viewed": last_viewed,
    }, 200


@job_interaction_routes.route("/<string:job_id>/interaction", methods=["POST"])
@token_required
def track_interaction(job_id):
    logger = get_logger()
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    if not interaction:
        new_interaction = JobInteraction(user_id=user_id, job_id=job_id)
        new_interaction.save()
        logger.info(
            "Created new interaction for job_id: %s by user_id: %s", job_id, user_id
        )

    return {"message": "Interaction tracked successfully"}, 200


@job_interaction_routes.route("/status/<string:job_id>", methods=["GET"])
@token_required
def get_interaction_status(job_id):
    logger = get_logger()
    user_id = request.user.get("user_id")
    interaction = JobInteraction.find(user_id, job_id)

    try:
        response = requests.get(f"{RAILS_API_URL}/job_posts/{job_id}")
        response.raise_for_status()
        job_post_data = response.json()
        logger.info("Fetched job post data for job_id: %s", job_id)
    except requests.exceptions.RequestException as e:
        logger.error(
            "Error fetching job post from Rails API for job_id %s: %s", job_id, e
        )
        return jsonify({"error": "Failed to fetch job post"}), 500

    if job_post_data:
        response = {
            "isPinned": interaction.is_pinned if interaction else False,
            "isSaved": interaction.is_saved if interaction else False,
            "hasFollowUp": interaction.has_follow_up if interaction else False,
            "viewCount": job_post_data.get("view_count", 0),
            "lastViewed": job_post_data.get("last_viewed"),
        }
    else:
        response = {
            "isPinned": False,
            "isSaved": False,
            "hasFollowUp": False,
            "viewCount": 0,
            "lastViewed": None,
        }

    logger.info("Returned interaction status for job_id: %s", job_id)
    return jsonify(response), 200
