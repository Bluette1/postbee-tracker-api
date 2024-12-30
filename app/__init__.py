from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from .config import get_config
from .routes import init_app
from .routes.tracking import tracking_routes
from app.routes.job_interactions import job_interaction_routes

db = MongoEngine()


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(get_config(config_name))

    db.init_app(app)

    CORS(app)

    init_app(app)

    app.register_blueprint(tracking_routes, url_prefix="/api/trackings")
    app.register_blueprint(job_interaction_routes, url_prefix='/api/jobs')

    return app
