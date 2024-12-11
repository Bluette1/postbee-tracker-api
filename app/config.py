import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_NAME', 'postbee_tracker'),  # Database name
        'host': os.getenv('MONGODB_HOST', 'localhost'),      # Host
        'port': int(os.getenv('MONGODB_PORT', 27017)),       # Port
        'username': os.getenv('MONGODB_USER'),               # Optional: Username for auth
        'password': os.getenv('MONGODB_PASS'),               # Optional: Password for auth
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MONGODB_SETTINGS['host'] = os.getenv('DEV_MONGODB_HOST', 'localhost')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGODB_SETTINGS['host'] = os.getenv('TEST_MONGODB_HOST', 'localhost')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class ProductionConfig(Config):
    """Production configuration."""
    MONGODB_SETTINGS['host'] = os.getenv('MONGODB_HOST') 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Dictionary to easily access the configuration
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Default configuration
def get_config(env='development'):
    return config_by_name.get(env, DevelopmentConfig)