from flask import Blueprint, jsonify, render_template, request
import typing as t
from utils import util
from flask import current_app as app
SUCCESS_MESSENGER = "sucsess"
FAIL_MESSENGER = "fail"
bp_upload = Blueprint("upload", __name__, template_folder="templates")

def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)

@bp_upload.route("/", methods=["GET"])
def upload_demo():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "upload.html"
    }
    return handle_before_response(response)

@bp_upload.route("/file", methods=["POST"])
def upload_file():
    status = SUCCESS_MESSENGER
    messenge = "Upload success"
    if 'file' not in request.files:
        return "No file part""HOME"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Check if the file upload was successful
    if not util.upload_file(file):
        messenge = "upload fail"
        status = FAIL_MESSENGER
    response = {
        "status": status,
        "message": messenge,
        "view": "home.html"
    }
    return handle_before_response(response,text=messenge)
