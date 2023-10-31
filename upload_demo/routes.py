from flask import Blueprint, jsonify, render_template, redirect, url_for
import typing as t
from config import SUPPORT_FRONT_END
SUCCESS_MESSENGER = "sucsess"

bp_upload = Blueprint("upload", __name__, template_folder="templates")

@bp_upload.route("/", methods=["GET"])
def upload_demo():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "upload.html"
    }
    return handle_before_response(response)

def handle_before_response(data, **context: t.Any):
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)
    
@bp_upload.route("/file", methods=["POST"])
def upload_file():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "home.html"
    }
    return handle_before_response(response)