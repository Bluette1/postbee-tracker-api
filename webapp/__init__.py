import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from celery import Celery
from webapp.config import get_config
from webapp.utils.logger import setup_logger

# Global instances
mongo = PyMongo()

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)

    # Load environment-specific configuration
    current_env = os.getenv("ENVIRONMENT", "development")
    config = get_config(current_env)

    app.config.from_object(config)
    config.init_app(app)

    # Setup logging
    setup_logger(app)

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize CORS
    CORS(app)

    # Initialize Celery
    celery = make_celery(app)

    with app.app_context():

        # Register blueprints
        from webapp.routes.job_interactions import job_interaction_routes
        from webapp.routes.tracking import tracking_routes

        app.register_blueprint(tracking_routes, url_prefix="/api/trackings")
        app.register_blueprint(job_interaction_routes, url_prefix="/api/jobs")

        # Import tasks after Celery is initialized
        import webapp.tasks.jobs

    return app, celery
