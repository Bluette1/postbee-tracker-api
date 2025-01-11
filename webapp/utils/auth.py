from functools import wraps

import requests
from flask import jsonify, request

from webapp.config import get_config

config = get_config()


def validate_token(token):
    response = requests.post(
        f"{config.RAILS_API_URL}/validate_token", json={"access_token": token}
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        token = token.split(" ")[1]  # Assuming "Bearer <token>"

        user_info = validate_token(token)

        if user_info is None:
            return jsonify({"message": "Invalid token"}), 401

        request.user = user_info
        return f(*args, **kwargs)

    return decorated
