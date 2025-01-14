import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from flask_mail import Mail

from webapp.consumer import (callback, compose_followup_message,
                             get_job_details, slugify)


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def mail_instance(app):
    with app.app_context():
        mail = Mail(app)
        yield mail


def test_slugify():
    assert (
        slugify("Software Engineer", "Tech Company") == "software-engineer-tech-company"
    )


def test_get_job_details_success():
    job_id = "12345"
    mock_job_data = {"title": "Software Engineer", "company_title": "Tech Company"}

    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_job_data)
        with patch("webapp.config.get_config") as mock_config:
            mock_config.return_value.RAILS_API_URL = "http://localhost:4200"
            title, link = get_job_details(job_id)
            assert title == "Software Engineer"
            assert (
                link == "http://localhost:4200/job-posts#software-engineer-tech-company"
            )


def test_compose_followup_message():
    followup_data = {
        "jobId": "12345",
        "status": "completed",
        "notes": "This is a note.",
        "nextStep": "Next step details.",
        "followUpDate": datetime(2025, 1, 1, 12, 0),  # Use a datetime object
    }

    with patch("webapp.consumer.get_job_details") as mock_get_job_details:
        mock_get_job_details.return_value = (
            "Software Engineer",
            "http://localhost:4200/job-posts#software-engineer",
        )
        message = compose_followup_message(followup_data)
        assert "Job Title: Software Engineer" in message
        assert "Job Link: http://localhost:4200/job-posts#software-engineer" in message
        assert "Status: completed" in message
        assert "Notes: This is a note." in message
        assert "Next Step: Next step details." in message
        assert "Follow-Up Date: January 01, 2025, 12:00 PM UTC" in message


def test_callback_success(mail_instance):
    followup_data = {
        "user_email": "test@example.com",
        "jobId": "12345",
        "status": "completed",
        "notes": "This is a note.",
    }

    with patch("webapp.consumer.compose_followup_message") as mock_compose:
        mock_compose.return_value = "Follow-up message."
        with patch("webapp.consumer.Mail.send") as mock_send:
            callback(
                MagicMock(),
                MagicMock(),
                MagicMock(),
                json.dumps(followup_data).encode(),
            )
            mock_send.assert_called_once()


def test_callback_failure(mail_instance):
    followup_data = {
        "user_email": "test@example.com",
        "jobId": "12345",
        "status": "completed",
        "notes": "This is a note.",
    }

    with patch("webapp.consumer.compose_followup_message") as mock_compose:
        mock_compose.return_value = "Follow-up message."
        with patch("webapp.consumer.Mail.send") as mock_send:
            mock_send.side_effect = Exception("Email error")
            callback(
                MagicMock(),
                MagicMock(),
                MagicMock(),
                json.dumps(followup_data).encode(),
            )
            # Ensure the logger captures the error (if you have logging set up)
            # You can mock the logger if needed
