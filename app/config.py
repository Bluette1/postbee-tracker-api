import os
from typing import Dict

class Config:
    """Base configuration."""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    DEBUG: bool = False
    TESTING: bool = False
    RAILS_API_URL: str = os.getenv("RAILS_API_URL", "http://localhost:3000")

    # Default MongoDB settings
    MONGODB_SETTINGS: Dict[str, str] = {
        "db": os.getenv("MONGODB_NAME", "postbee_tracker"),
        "host": os.getenv("MONGODB_HOST", "localhost"),
        "port": int(os.getenv("MONGODB_PORT", "27017")),
        "username": os.getenv("MONGODB_USER"),
        "password": os.getenv("MONGODB_PASS"),
    }


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