# pylint: skip-file
import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from app.config import get_config
from app.utils.logger import setup_logger
from app.celery_config import make_celery

mongo = PyMongo()
celery = None

def create_app():
    app = Flask(__name__)

    current_env = os.getenv("ENVIRONMENT", "development")
    config = get_config(current_env)

    app.config.from_object(config)
    config.init_app(app)

    setup_logger(app)
    app.logger.info(f"Starting application in {current_env} mode")

    # Initialize MongoDB
    mongo.init_app(app)
    app.logger.info("MongoDB initialized")

    # Initialize Celery
    global celery
    celery = make_celery(app)
    app.logger.info("Celery initialized")

    CORS(app)

    with app.app_context():
        from app.routes.job_interactions import job_interaction_routes
        from app.routes.tracking import tracking_routes

        app.register_blueprint(tracking_routes, url_prefix="/api/trackings")
        app.register_blueprint(job_interaction_routes, url_prefix="/api/jobs")

        app.logger.info("All blueprints registered")

        return app