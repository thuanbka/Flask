from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from entity.word_toeic import WordToeic
from entity.set_question import SetQuestion
from entity.user import User
import typing as t
from flask import current_app as app
from my_app import db
from utils import handle_question_word
import json

bp_question_toeic = Blueprint(
    "question_toeic", __name__, template_folder="templates")
SUCCESS_MESSENGER = "sucsess"
EXPIRED_TIME = 3600


@bp_question_toeic.route("/", methods=["GET"])
def home_question_toeic():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "HOME question TOEIC",
        "view": "home_question_toeic.html"
    }
    return handle_before_response(response)


@bp_question_toeic.route("/generate_question_user", methods=["GET"])
def get_generate_question_user():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Please login!!",
        "view": "generate_question_user.html"
    }
    return handle_before_response(response)


@bp_question_toeic.route('/generate_question_user', methods=['POST'])
def set_generate_question_user():
    try:
        SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if not data or 'username' not in data:
            return handle_before_response({'error': 'Invalid data'}), 401
        else:
            list_word = db.session.query(WordToeic).all()
            result_generate = handle_question_word.create_data_question_user(
                db=db, user_name=data["username"], len_questions=len(list_word), number_sets=30)
            if result_generate:
                if SUPPORT_FRONT_END:
                    return handle_before_response({'message': 'Generate successful'})
                else:
                    return handle_before_response({'message': 'Generate successful'})
            else:
                return handle_before_response({'error': 'Generate question Failed'}), 405
    except Exception as ex:
        print("Error: %s" % (str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500


@bp_question_toeic.route("/get_test_question", methods=["GET"])
def get_test_question():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "WELCOME to WELCOME",
    }
    if "response" in request.args:
        response = json.loads(request.args.get("response"))
        ### THIS IS TRICK DATA PLEASE FIX IT#######
    response["user_name"] = "thuan"
    if "user_name" in request.args:
        response["user_name"] = request.args["user_name"]
    user = User()
    list_set_questions = []
    if response != None and "user_name" in response:
        user = (
            db.session.query(User)
            .filter(User.username == response["user_name"])
            .first()
        )
        if user != None:
            list_set_questions = db.session.query(SetQuestion).filter(
                SetQuestion.user_id == user.id).order_by(SetQuestion.name_set).all()
            # Convert a list of SetQuestion objects to dictionaries
            list_set_questions = [set_question.to_dict()
                                  for set_question in list_set_questions]
        else:
            return handle_before_response({'error': 'Invalid username:%s' % response["user_name"]}), 401
    else:
        user.setUsername("Noname_user")
    response["view"] = "test_question.html"
    return handle_before_response(response, user=user, number_question=len(list_set_questions), list_set_questions=list_set_questions)


@bp_question_toeic.route("/test_question_toeic", methods=["GET"])
def get_test_question_toeic():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "WELCOME to WELCOME",
    }
    if response != None and "user_name" in request.args and "list_question" in request.args:
        user_name = request.args["user_name"]
        response["view"] = "test_question_toeic.html"
        list_questions = request.args["list_question"]
        set_question_id = request.args["set_question_id"]
        return handle_before_response(response, user_name=user_name, list_questions=list_questions, set_question_id=set_question_id)
    else:
        return handle_before_response({'error': 'Can not get test toeic'}), 403


@bp_question_toeic.route('/update_result', methods=['POST'])
def update_result():
    try:
        SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if not data or 'username' not in data and "result" in data and "set_question_id" in data:
            return handle_before_response({'error': 'Invalid data'}), 401
        else:
            set_question = SetQuestion.query.get(data["set_question_id"])
            if set_question:
                set_question.set_result_status(data["result"])
                db.session.commit()
                return handle_before_response({"message": "Update result successfully!"}), 200
            else:
                return handle_before_response({"message": "Update result failed!!"}), 404
    except Exception as ex:
        print("Error: %s" % (str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500


def handle_before_response(data, **context: t.Any):
    SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
    if SUPPORT_FRONT_END and 'view' in data:
        if "token" in data:
            session["token"] = data["token"]
        return render_template(data['view'], **context)
    else:
        if 'view' in data:
            del data["view"]
        return jsonify(data)
