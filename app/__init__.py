from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.config import get_config
import os

mongo = PyMongo()


def create_app():

    app = Flask(__name__)

    current_env = os.getenv("ENVIRONMENT", "development")
    config = get_config(current_env)

    app.config.from_object(config)
    config.init_app(app)

    global mongo
    mongo.init_app(app)

    CORS(app)

    with app.app_context():
        from .routes.tracking import tracking_routes
        from app.routes.job_interactions import job_interaction_routes

        app.register_blueprint(tracking_routes, url_prefix="/api/trackings")
        app.register_blueprint(job_interaction_routes, url_prefix="/api/jobs")

        return app
