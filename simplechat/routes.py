from flask import Blueprint, render_template, jsonify,request
from flask import current_app as app
import typing as t

bp_simplechat =Blueprint("simple_chat",__name__, template_folder="templates")
SUCCESS_MESSENGER = "sucsess"

@bp_simplechat.route("/simple", methods=["GET"])
def get_simple_chat():
    ip_address = request.access_route
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "SIMPLECHAT!!",
        "ip_address": ip_address,
        "view": "home.html"
    }
    return handle_before_response(response,text=response["message"])
def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)