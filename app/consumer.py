import pika
import json
from flask import Flask, current_app
from flask_mail import Message, Mail
import requests
from app.config import get_config

config = get_config()
API_BASE_URL = config.RAILS_API_URL

mail = Mail()

app = Flask(__name__)


def get_job_details(job_id):
    """Fetch job details based on job ID from the external Rails API."""
    response = requests.get(f"{API_BASE_URL}/jobs/{job_id}")
    if response.status_code == 200:
        job_data = response.json()
        job_title = job_data.get("title")
        job_link = job_data.get("link")
        return job_title, job_link
    else:
        current_app.logger.error(
            f"Failed to fetch job details for job ID {job_id}: {response.status_code}"
        )
        return None, None


def compose_followup_message(followup_data):
    """Compose the follow-up message based on the follow-up data."""
    message_parts = []

    # Fetch job title and link using the job ID
    job_title, job_link = get_job_details(followup_data["jobId"])
    if job_title and job_link:
        message_parts.append(f"Job Title: {job_title}")
        message_parts.append(f"Job Link: {job_link}")

    # Include the status of the follow-up
    message_parts.append(f"Status: {followup_data['status']}")

    # Include notes if available
    if followup_data.get("notes"):
        message_parts.append(f"Notes: {followup_data['notes']}")

    # Include the next steps if available
    if followup_data.get("nextStep"):
        message_parts.append(f"Next Step: {followup_data['nextStep']}")

    # Include the follow-up date if available
    if followup_data.get("followUpDate"):
        message_parts.append(f"Follow-Up Date: {followup_data['followUpDate']}")

    # Combine all parts into a single message
    return "\n".join(message_parts)


def start_consumer():
    """Start the Pika consumer."""
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="followup_notifications")  # Ensure the queue exists

    channel.basic_consume(
        queue="followup_notifications", on_message_callback=callback, auto_ack=True
    )

    app.logger.info("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def callback(ch, method, properties, body):
    """Callback function to handle incoming messages."""
    followup_data = json.loads(body)
    user_email = followup_data["user_email"]

    message = compose_followup_message(followup_data)

    # Send email using Flask-Mail (or any other method)
    msg = Message(subject="Follow-Up Notification", recipients=[user_email])
    msg.body = message

    try:
        mail.send(msg)
        current_app.logger.info(f"Follow-up notification sent to {user_email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send notification: {e}")
