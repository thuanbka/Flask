from flask import Blueprint, render_template, jsonify,request, session
from flask import current_app as app
import typing as t
from dashboard import routes
from . import bp_simplechat

SUCCESS_MESSENGER = "sucsess"

@bp_simplechat.route("/simple", methods=["GET"])
def get_simple_chat():
    if app.config["SUPPORT_FRONT_END"]:
        token = session.get("token", "")
    else:
        token = request.headers.get('Authorization')
    verification_result = routes.verify_token(token=token)
    if 'username' in verification_result:
        session["name"] = verification_result['username']
        ip_address = request.access_route
        response = {
            "status": SUCCESS_MESSENGER,
            "message": "SIMPLECHAT!!",
            "ip_address": ip_address,
            "view": "chat.html"
        }
        return handle_before_response(response)
    else:
        return handle_before_response({'error': verification_result}), 401

def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)