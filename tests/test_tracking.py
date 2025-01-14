from unittest.mock import patch

import pytest
from flask import Flask

from webapp.routes.tracking import tracking_routes


# Create a Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(tracking_routes)  # Register the tracking_routes blueprint
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_track_interaction_valid_token(client):
    with patch("webapp.utils.auth.validate_token") as mock_validate:
        mock_validate.return_value = {"user_id": "test_user"}  # Simulate valid token
        response = client.post(
            "/tracking/", headers={"Authorization": "Bearer valid_token"}
        )
        assert response.status_code == 201
        assert response.get_json() == {
            "message": "User tracked successfully",
            "user_id": "test_user",
        }


def test_track_interaction_invalid_token(client):
    with patch("webapp.utils.auth.validate_token") as mock_validate:
        mock_validate.return_value = None  # Simulate invalid token
        response = client.post(
            "/tracking/", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert response.get_json() == {"message": "Invalid token"}


def test_get_tracking_valid_token(client):
    with patch("webapp.utils.auth.validate_token") as mock_validate:
        mock_validate.return_value = {"user_id": "test_user"}  # Simulate valid token
        response = client.get(
            "/tracking/1", headers={"Authorization": "Bearer valid_token"}
        )
        assert response.status_code == 200
        assert response.get_json() == {
            "message": "Tracking detail for ID 1",
            "user_id": "test_user",
        }


def test_get_tracking_invalid_token(client):
    with patch("webapp.utils.auth.validate_token") as mock_validate:
        mock_validate.return_value = None  # Simulate invalid token
        response = client.get(
            "/tracking/1", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert response.get_json() == {"message": "Invalid token"}
