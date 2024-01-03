from flask import Blueprint, jsonify, render_template, session, request, send_file
import typing as t
from flask import current_app as app
from dashboard import routes

SUCCESS_MESSENGER = "sucsess"
FAIL_MESSENGER = "fail"
bp_download = Blueprint("download", __name__, template_folder="templates")

def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)

@bp_download.route("/", methods=["GET"])
def download_demo():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "demo_download.html"
    }
    return handle_before_response(response)

@bp_download.route("/demo", methods=["POST"])
def download_file():
    status = SUCCESS_MESSENGER
    messenge = "Download to local success."
    if app.config["SUPPORT_FRONT_END"]:
        token = session.get("token", "")     
    else:
        token = request.headers.get('Authorization')
    verification_result = routes.verify_token(token=token)
    ip_address = request.access_route
    if 'username' in verification_result:
        role = verification_result['role']
        if role == "admin":
           file_path = '../resources/turtle.jpeg'
           return send_file(file_path, as_attachment=True)
        else:
            messenge = "Download to local Failed. User is not admin"
        
    else:
        messenge = "Download to local Failed. User not authentication"

    response = {
            "status": status,
            "message": messenge,
            "ip_address": ip_address
        }
    return handle_before_response(response)