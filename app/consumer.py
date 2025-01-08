import json
import pika
import requests
from flask import Flask, current_app
from flask_mail import Mail, Message
from app.config import get_config

# Initialize Flask app and Mail
app = Flask(__name__)
config = get_config()
app.config.from_object(config)
mail = Mail(app)

API_BASE_URL = config.RAILS_API_URL

def get_job_details(job_id):
    """Fetch job details based on job ID from the external Rails API."""
    try:
        response = requests.get(f"{API_BASE_URL}/jobs/{job_id}", timeout=10)
        response.raise_for_status()

        job_data = response.json()
        job_title = job_data.get("title")
        job_link = job_data.get("link")
        return job_title, job_link
    except requests.exceptions.RequestException as e:
        current_app.logger.error(
            f"Failed to fetch job details for job ID {job_id}: {e}"
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

def callback(ch, method, properties, body):
    """Callback function to handle incoming messages."""
    followup_data = json.loads(body)
    user_email = followup_data["user_email"]

    message = compose_followup_message(followup_data)

    # Send email using Flask-Mail
    msg = Message(subject="Follow-Up Notification", recipients=[user_email])
    msg.body = message

    try:
        with app.app_context():  # Ensure app context is available for sending email
            mail.send(msg)
        current_app.logger.info(f"Follow-up notification sent to {user_email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send notification: {e}")

def start_consumer():
    """Start the Pika consumer."""
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="followup_notifications")  # Ensure the queue exists

    channel.basic_consume(
        queue="followup_notifications", on_message_callback=callback, auto_ack=True
    )

    with app.app_context():  # Start app context for logging
        app.logger.info("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
