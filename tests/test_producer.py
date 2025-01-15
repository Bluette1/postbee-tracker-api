import json
from unittest.mock import MagicMock, patch

from webapp.producer import publish_followup_notification


def test_publish_followup_notification():
    followup_data = {
        "user_email": "test@example.com",
        "jobId": "12345",
        "status": "completed",
        "notes": "This is a note.",
        "nextStep": "Next step details.",
        "followUpDate": "2025-01-01",
    }

    with patch("pika.BlockingConnection") as mock_connection:
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        publish_followup_notification(followup_data)

        # Assert the queue declaration
        mock_channel.queue_declare.assert_called_once_with(
            queue="followup_notifications"
        )

        # Assert the message publishing
        expected_message = json.dumps(
            {
                "user_email": "test@example.com",
                "jobId": "12345",
                "status": "completed",
                "notes": "This is a note.",
                "nextStep": "Next step details.",
                "followUpDate": "2025-01-01",
            }
        )
        mock_channel.basic_publish.assert_called_once_with(
            exchange="", routing_key="followup_notifications", body=expected_message
        )

        # Assert connection close
        mock_connection.return_value.close.assert_called_once()
