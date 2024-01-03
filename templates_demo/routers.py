from flask import Blueprint, jsonify, render_template
import typing as t
from flask import current_app as app

SUCCESS_MESSENGER = "sucsess"
FAIL_MESSENGER = "fail"
bp_template_demo = Blueprint("template", __name__, template_folder="templates")

def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)

@bp_template_demo.route("/touchscreen", methods=["GET"])
def template_touchscreen():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "touchscreen.html"
    }
    return handle_before_response(response)

@bp_template_demo.route("/heart", methods=["GET"])
def template_heart():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "test.html"
    }
    return handle_before_response(response)

@bp_template_demo.route("/fire_flower", methods=["GET"])
def template_fire_work():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Upload a file",
        "view": "fire_flower.html"
    }
    return handle_before_response(response)