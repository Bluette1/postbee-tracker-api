#!/usr/bin/env python3
from webapp import create_app

def main():
    flask_app, celery_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()