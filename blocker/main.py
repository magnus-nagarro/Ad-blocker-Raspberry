import requests
from flask import Flask, jsonify, request, Response
from MongoDB import mongodb


class Backend(mongodb):
    def __init__(self) -> None:
        self.db = mongodb()

    def create_app(self):
        app = Flask(__name__)

        @app.route("/test", methods=["GET"])
        def test():
            return "Hello World"

        @app.route("/add", methods=["POST"])
        def add_links():
            link = request.args.get('link')
            if not link:
                return jsonify("Please provide a link!")
            success = self.db.add_links(link)
            return jsonify(f"success: {success}")

        return app


if __name__ == "__main__":
    try:
        backend = Backend()
        app = backend.create_app()
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"An error occured, error: {e}")
    finally:
        print("Exiting... Bye Bye :)")
