from celery import shared_task
from flask import current_app

from webapp.producer import publish_followup_notification


@shared_task(name="app.tasks.jobs.send_followup_notification")
def send_followup_notification(followup_data):
    publish_followup_notification(followup_data)
    current_app.logger.info(
        f"Follow-up notification published for job ID: {followup_data['jobId']}"
    )
