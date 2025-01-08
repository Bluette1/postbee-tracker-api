from celery import Celery
from flask import current_app

from app.producer import publish_followup_notification

celery = Celery("tasks", broker=current_app.config["CELERY_BROKER_URL"])


@celery.task
def send_followup_notification(followup_data):
    """Send follow-up notification by publishing to RabbitMQ."""
    publish_followup_notification(followup_data)
    current_app.logger.info(
        f"Follow-up notification published for job ID: {followup_data['jobId']}"
    )
