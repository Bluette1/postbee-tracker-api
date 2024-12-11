from flask import Flask
from flask_mongoengine import MongoEngine
from .config import get_config

db = MongoEngine()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    app.config.from_object(get_config(config_name))

    db.init_app(app)

    with app.app_context():
        from . import routes 
        

    return app