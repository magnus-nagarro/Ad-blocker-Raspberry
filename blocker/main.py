import requests
from flask import Flask, jsonify, request, Response


class Backend:
    def __init__(self) -> None:
        pass

    def create_app(self):
        app = Flask(__name__)

        @app.route('/test', methods=['GET'])
        def test():
            return "Hello World"

        return app


if __name__ == "__main__":
    backend = Backend()
    app = backend.create_app()
    app.run(host='0.0.0.0', port=8080)
