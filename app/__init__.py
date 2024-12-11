from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine

from .config import get_config
from .routes.tracking import tracking_routes

db = MongoEngine()


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(get_config(config_name))

    db.init_app(app)

    CORS(app)

    from .routes import init_app

    init_app(app)

    app.register_blueprint(tracking_routes, url_prefix="/api/trackings")

    return app
