# app/utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import request

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url if request else "No URL"
        record.remote_addr = request.remote_addr if request else "No IP"
        record.method = request.method if request else "No method"
        return super().format(record)

def setup_logger(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up file handler for general logs
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10485760,  # 10MB
        backupCount=10
    )

    # Set up file handler for errors
    error_file_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )

    # Create formatters and add it to handlers
    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(method)s %(levelname)s: %(message)s'
    )
    
    file_handler.setFormatter(request_formatter)
    error_file_handler.setFormatter(request_formatter)

    # Set log levels
    file_handler.setLevel(logging.INFO)
    error_file_handler.setLevel(logging.ERROR)

    # Add handlers to the app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_file_handler)
    
    # Set base logging level
    app.logger.setLevel(logging.INFO)

    # Log startup
    app.logger.info('Application startup')