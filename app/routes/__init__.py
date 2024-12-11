from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/health", methods=["GET"])
def health_check():
    return (
        jsonify({"status": "healthy", "message": "PostBee Tracker API is running"}),
        200,
    )


def init_app(app):
    app.register_blueprint(main)
