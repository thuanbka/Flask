from utils import util
from flask import Flask, request, session
import posixpath
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO

socketio = SocketIO()

def cdn_url_builder(_error, endpoint, values):
    if endpoint != "cdn":
        return None
    from flask import current_app as app
    return posixpath.join(app.config["CDN_DOMAIN"], "static", values["filename"])

def create_app():
    license_remote = util.get_license("license_test")
    license_local = util.get_license_local("license")
    if license_remote != None and license_remote != license_local:
        print("License not match")
        return None
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.url_build_error_handlers.append(cdn_url_builder)
    # Load environment variables from .env file during testing
    if app.config['TESTING']:
        load_dotenv()

    app.config['SECRET_KEY'] = util.sha256_encode(os.getenv("SECRET_KEY"))
    from dashboard.routes import bp_dashboard
    from upload_demo.routes import bp_upload
    from simplechat import bp_simplechat

    app.register_blueprint(bp_dashboard)
    app.register_blueprint(bp_upload, url_prefix="/upload")
    app.register_blueprint(bp_simplechat, url_prefix="/chat")
    socketio.init_app(app)

    # @app.before_request
    # def before_request_func() -> None:
    #     if app.config["SUPPORT_FRONT_END"]:
    #         request.headers['Authorization'] = session.get('token', '')
    return app
