from __init__ import *


class Backend():
    def __init__(self) -> None:
        self.db = mongodb()

    # Main flask function -> Flask
    def create_app(self):
        app = Flask(__name__)

        # Test Endpoint, call with /test => [GET]
        @app.route("/test", methods=["GET"])
        def test():
            return jsonify({"success": True,
                            "message": "Hello World"})

        # Endpoint to add Links to the database, call with /add?link="" => [POST]
        @app.route("/add", methods=["POST"])
        def add_links():
            link = request.args.get('link')
            # If request has no link we return an error
            if not link:
                return jsonify({"success": False,
                                "error": "Please provide a link!"})
            success = self.db.add_links(link)
            return jsonify(success)

        # Endpoint to start the addblocker, call with /start => [POST]
        @app.route("/start", methods=["POST"])
        def start():
            success = self.db.blocker_on_off(True)
            return jsonify({"running": True})

        # Endpoint to stop the addblocker, call with /stop => [POST]
        @app.route("/stop", methods=["POST"])
        def stop():
            success = self.db.blocker_on_off(False)
            return jsonify({"running": False})

        # Endpoint to return all links in the blocked list, call with /blocked => [GET]
        @app.route("/blocked", methods=["GET"])
        def blocked():
            return_buffer = self.db.return_links()
            return jsonify(return_buffer)

        # Endpoint to delete a link from the database, call with /delete?link="" => [DELETE]
        @app.route("/delete", methods=["DELETE"])
        def delete():
            link = request.args.get("link")
            # If request has no link we return an error
            if not link:
                return jsonify({"success": False,
                                "error": "Please provide a link!"})
            success = self.db.delete_links(link)
            return jsonify(success)

        return app


if __name__ == "__main__":
    try:
        backend = Backend()
        app = backend.create_app()
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"An error occured, error: {e}")
    finally:
        print("Exiting...")
