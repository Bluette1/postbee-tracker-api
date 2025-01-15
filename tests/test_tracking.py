import unittest
from unittest.mock import patch

from webapp import create_app


class TrackingTestCase(unittest.TestCase):
    def setUp(self):
        self.app, self.celery = create_app()  # Initialize the app and celery
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()  # Pop the application context

    def test_track_interaction_valid_token(self):
        with patch("webapp.utils.auth.validate_token") as mock_validate:
            mock_validate.return_value = {
                "user_id": "test_user"
            }  # Simulate valid token
            response = self.client.post(
                "/api/trackings/", headers={"Authorization": "Bearer valid_token"}
            )
            assert response.status_code == 201
            assert response.get_json() == {
                "message": "User tracked successfully",
                "user_id": "test_user",
            }

    def test_track_interaction_invalid_token(self):
        with patch("webapp.utils.auth.validate_token") as mock_validate:
            mock_validate.return_value = None  # Simulate invalid token
            response = self.client.post(
                "/api/trackings/", headers={"Authorization": "Bearer invalid_token"}
            )
            assert response.status_code == 401
            assert response.get_json() == {"message": "Invalid token"}

    def test_get_tracking_valid_token(self):
        with patch("webapp.utils.auth.validate_token") as mock_validate:
            mock_validate.return_value = {
                "user_id": "test_user"
            }  # Simulate valid token
            response = self.client.get(
                "/api/trackings/1", headers={"Authorization": "Bearer valid_token"}
            )
            assert response.status_code == 200
            assert response.get_json() == {
                "message": "Tracking detail for ID 1",
                "user_id": "test_user",
            }

    def test_get_tracking_invalid_token(self):
        with patch("webapp.utils.auth.validate_token") as mock_validate:
            mock_validate.return_value = None  # Simulate invalid token
            response = self.client.get(
                "/api/trackings/1", headers={"Authorization": "Bearer invalid_token"}
            )
            assert response.status_code == 401
            assert response.get_json() == {"message": "Invalid token"}
