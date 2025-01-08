import os
from typing import Dict


class Config:
    """Base configuration."""

    DEBUG: bool = False
    TESTING: bool = False
    RAILS_API_URL: str = os.getenv("RAILS_API_URL", "http://localhost:3000")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:4200")

    # Default MongoDB settings
    MONGODB_SETTINGS: Dict[str, str] = {
        "db": os.getenv("MONGODB_NAME", "postbee_tracker"),
        "host": os.getenv("MONGODB_HOST", "localhost"),
        "port": int(os.getenv("MONGODB_PORT", "27017")),
        "username": os.getenv("MONGODB_USER"),
        "password": os.getenv("MONGODB_PASS"),
    }

    # MongoDB URI for connection
    MONGO_URI: str = os.getenv("MONGO_URI", None)

    # Celery Configuration
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "pyamqp://guest@localhost//")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

    # Additional Celery configurations
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TIMEZONE = "UTC"
    CELERY_ENABLE_UTC = True

    # Mail Settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))  # 465 for SSL
    MAIL_USE_TLS = bool(os.getenv("MAIL_USE_TLS", "True"))  # False if using SSL
    MAIL_USE_SSL = bool(os.getenv("MAIL_USE_SSL", "False"))  # True if using SSL
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    @classmethod
    def init_app(cls, app):
        """Initialize the application with the proper MongoDB URI."""
        if cls.MONGO_URI is None:
            cls.MONGO_URI = cls.construct_mongodb_uri(cls.MONGODB_SETTINGS)

        # Set the MONGO_URI in the app's config
        app.config["MONGO_URI"] = cls.MONGO_URI
        print(
            "Initialized MONGO_URI in app config:", app.config["MONGO_URI"]
        )  # Debugging

    @staticmethod
    def construct_mongodb_uri(settings: Dict[str, str]) -> str:
        """Construct MongoDB URI from settings."""
        uri = "mongodb://"
        if settings.get("username") and settings.get("password"):
            uri += f"{settings['username']}:{settings['password']}@"
        uri += f"{settings['host']}:{settings['port']}/{settings['db']}"
        return uri


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG: bool = True
    MONGODB_SETTINGS: Dict[str, str] = {
        **Config.MONGODB_SETTINGS,
        "host": os.getenv("DEV_MONGODB_HOST", "localhost"),
    }
    RAILS_API_URL: str = os.getenv("DEV_RAILS_API_URL", "http://localhost:3000")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING: bool = True
    MONGODB_SETTINGS: Dict[str, str] = {
        **Config.MONGODB_SETTINGS,
        "host": os.getenv("TEST_MONGODB_HOST", "localhost"),
    }
    RAILS_API_URL: str = os.getenv("TEST_RAILS_API_URL", "http://localhost:3000")


class ProductionConfig(Config):
    """Production configuration."""

    MONGODB_SETTINGS: Dict[str, str] = {
        **Config.MONGODB_SETTINGS,
        "host": os.getenv("MONGODB_HOST"),
    }
    RAILS_API_URL: str = os.getenv("RAILS_API_URL")


# Dictionary to easily access the configuration
config_by_name: Dict[str, type] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


# Default configuration
def get_config(env: str = "development") -> Config:
    """Get the configuration class based on the environment."""
    return config_by_name.get(env, DevelopmentConfig)
