import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify, request
from webapp.utils.auth import token_required, validate_token

# Create a Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/protected', methods=['GET'])
    @token_required
    def protected():
        return jsonify({"message": "Access granted", "user": request.user})

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_validate_token_success():
    with patch('webapp.utils.auth.requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"user_id": "test_user"})
        result = validate_token("valid_token")
        assert result == {"user_id": "test_user"}

def test_validate_token_failure():
    with patch('webapp.utils.auth.requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=401)  # Unauthorized
        result = validate_token("invalid_token")
        assert result is None

def test_token_required_missing_token(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.get_json() == {"message": "Token is missing"}

def test_token_required_invalid_token(client):
    with patch('webapp.utils.auth.validate_token') as mock_validate:
        mock_validate.return_value = None  # Simulate invalid token
        response = client.get('/protected', headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        assert response.get_json() == {"message": "Invalid token"}

def test_token_required_valid_token(client):
    with patch('webapp.utils.auth.validate_token') as mock_validate:
        mock_validate.return_value = {"user_id": "test_user"}  # Simulate valid token
        response = client.get('/protected', headers={"Authorization": "Bearer valid_token"})
        assert response.status_code == 200
        assert response.get_json() == {"message": "Access granted", "user": {"user_id": "test_user"}}