from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.updates import updates_bp
from routes.deadlines import deadlines_bp
from routes.users import users_bp
from routes.external import external_bp

def create_app():
    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(updates_bp,   url_prefix="/api/updates")
    app.register_blueprint(deadlines_bp, url_prefix="/api/deadlines")
    app.register_blueprint(users_bp,     url_prefix="/api/users")
    app.register_blueprint(external_bp,  url_prefix="/api/external")

    @app.route("/api/health")
    def health():
        return {"status": "ok", "app": "Fahamu API"}

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
