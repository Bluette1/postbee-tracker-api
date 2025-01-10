from webapp import create_app

flask_app, celery = create_app()

if __name__ == '__main__':
    flask_app.run()
