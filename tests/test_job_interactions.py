import unittest
from unittest.mock import MagicMock, patch

import requests
from flask import json

from webapp import create_app
from webapp.models.job_interaction import JobInteraction


class JobInteractionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app, self.celery = create_app()  # Initialize the app and celery
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()  # Pop the application context

    @patch("webapp.routes.job_interactions.requests.post")  # Mock requests.post
    def test_track_view_error(self, mock_post):
        job_id = "job_id"

        # Simulate an error from the Rails API
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        response = self.client.post(
            f"/api/jobs/{job_id}/view", headers={"Authorization": "Bearer token"}
        )

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Failed to update view count")

    @patch("webapp.utils.auth.validate_token")  # Mock validate_token
    @patch("requests.post")
    @patch("requests.get")
    def test_create_follow_up(self, mock_get, mock_post, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "123",
            "email": "test@example.com",
        }
        mock_post.return_value = MagicMock(
            status_code=200, json=lambda: {"user_email": "test@example.com"}
        )

        data = {"followUpDate": "2025-01-21T10:00:00Z", "jobId": "job_id"}

        response = self.client.post(
            "/api/jobs/job_id/follow-ups",
            headers={"Authorization": "Bearer token"},
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("user_email", json.loads(response.data))

    @patch("webapp.routes.job_interactions.requests.post")  # Mock requests.post
    def test_track_view(self, mock_post):
        job_id = "job_id"

        # Mock the response from the Rails API
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {"view_count": 15, "last_viewed": "2025-01-13T10:00:00Z"},
        )

        response = self.client.post(
            f"/api/jobs/{job_id}/view", headers={"Authorization": "Bearer token"}
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "View tracked successfully")
        self.assertEqual(data["view_count"], 15)
        self.assertEqual(data["last_viewed"], "2025-01-13T10:00:00Z")

    @patch("webapp.utils.auth.validate_token")  # Mock validate_token
    @patch("requests.get")
    def test_get_follow_up(self, mock_get, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "123",
            "email": "test@example.com",
        }

        # Mock the response to return the follow-up data
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"followUpDate": "2025-01-21T10:00:00Z", "jobId": "job_id"},
        )

        response = self.client.get(
            "/api/jobs/job_id/follow-ups", headers={"Authorization": "Bearer token"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data),
            {"followUpDate": "2025-01-21T10:00:00Z", "jobId": "job_id"},
        )

    @patch("webapp.utils.auth.validate_token")  # Mock validate_token
    @patch("requests.get")
    def test_get_interaction_status(self, mock_get, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "123",
            "email": "test@example.com",
        }

        # Mock the response to return the interaction status
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"view_count": 10, "last_viewed": "2025-01-13T10:00:00Z"},
        )

        response = self.client.get(
            "/api/jobs/status/job_id", headers={"Authorization": "Bearer token"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check the structure of the response data
        self.assertIn("viewCount", data)  # Ensure 'viewCount' key exists
        self.assertEqual(data["viewCount"], 10)

    @patch("webapp.utils.auth.validate_token")  # Mock validate_token
    def test_toggle_pin(self, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "123",
            "email": "test@example.com",
        }

        response = self.client.post(
            "/api/jobs/job_id/pin", headers={"Authorization": "Bearer token"}
        )
        self.assertEqual(response.status_code, 200)

    @patch("webapp.utils.auth.validate_token")  # Mock validate_token
    def test_toggle_save(self, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "123",
            "email": "test@example.com",
        }

        response = self.client.post(
            "/api/jobs/job_id/save", headers={"Authorization": "Bearer token"}
        )
        self.assertEqual(response.status_code, 200)

    @patch("webapp.utils.auth.validate_token")  # Mock the token validation
    @patch("webapp.models.JobInteraction")  # Mock the JobInteraction model
    def test_get_follow_up_not_found(self, mock_job_interaction, mock_validate_token):
        mock_validate_token.return_value = {
            "user_id": "user_id",
            "email": "test@example.com",
        }

        # Set up the mock to return None for the find method
        mock_job_interaction.find.return_value = None

        response = self.client.get(
            "/api/jobs/job_id/follow-ups", headers={"Authorization": "Bearer token"}
        )

        # Assert the response status code and message
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Follow-up not found")


if __name__ == "__main__":
    unittest.main()
