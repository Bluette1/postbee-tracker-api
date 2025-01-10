#!/bin/bash

# Set environment variables
export FLASK_APP=run.py
export FLASK_ENV=development
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Start the Flask application
python3 run.py