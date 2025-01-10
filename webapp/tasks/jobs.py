from celery import shared_task
from flask import current_app
from celery.utils.log import get_task_logger
from webapp.producer import publish_followup_notification

logger = get_task_logger(__name__)


@shared_task(name="app.tasks.jobs.send_followup_notification")
def send_followup_notification(followup_data):
    logger.info(f"Sending follow-up notification  for job: {followup_data}")
    publish_followup_notification(followup_data)
    current_app.logger.info(
        f"Follow-up notification published for job ID: {followup_data['jobId']}"
    )
