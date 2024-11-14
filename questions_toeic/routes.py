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
        "message": "Get generate question user success!!",
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
            len_list_word = db.session.query(WordToeic).count()
            result_generate = handle_question_word.create_data_question_user(
                db=db, user_name=data["username"], len_questions=len_list_word, number_sets=30)
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
        "message": "get test question",
    }
    ### THIS IS TRICK DATA PLEASE FIX IT#######
    user_name = "thuan"
    if "user_name" in request.args:
        user_name = request.args["user_name"]
    response["view"] = "test_question.html"
    return handle_before_response(response, user_name=user_name)


@bp_question_toeic.route("/get_test_question", methods=["POST"])
def post_test_question():
    try:
        response = {
            "status": SUCCESS_MESSENGER,
            "message": "post test question",
        }
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400
        if "user_name" in data:
            response["user_name"] = data["user_name"]
            list_set_questions = []
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
                response["list_set_questions"] = list_set_questions
                return handle_before_response(response)
            else:
                return handle_before_response({'error': 'Invalid username:%s' % response["user_name"]}), 401
        else:
            return handle_before_response({'error': 'Miss username in request.'}), 401
    except Exception as ex:
        print("Error: %s" % (str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500


@bp_question_toeic.route("/test_question_toeic", methods=["GET"])
def get_test_question_toeic():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "WELCOME to WELCOME",
    }
    if response != None and "user_name" in request.args and "set_question_id" in request.args:
        response["view"] = "test_question_toeic.html"
        set_question_id = request.args["set_question_id"]
        user_name = request.args["user_name"]
        return handle_before_response(response, set_question_id=set_question_id, user_name=user_name)
    else:
        return handle_before_response({'error': 'Can not get test toeic'}), 403


@bp_question_toeic.route('/test_question_toeic', methods=['POST'])
def post_test_question_toeic():
    try:
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if not data or "set_question_id" not in data:
            return handle_before_response({'error': 'Invalid data'}), 401
        else:
            set_question = SetQuestion.query.get(data["set_question_id"])
            if set_question:
                response = {
                    "status": SUCCESS_MESSENGER,
                    "message": "Get set question success!",
                    "set_question": set_question.to_dict()
                }
                return handle_before_response(response)
            else:
                return handle_before_response({"message": "Get set question failed!!"}), 404
    except Exception as ex:
        print("Error: %s" % (str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500


@bp_question_toeic.route('/list_vocabulary', methods=['POST'])
def get_list_vocabulary():
    try:
        ## Todo: Request need a token##
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if (not data) or ('token' not in data):
            return handle_before_response({'error': 'Invalid data'}), 401
        else:
            list_vocabulary = db.session.query(WordToeic).all()
            if len(list_vocabulary) > 0:
                response = {
                    "status": SUCCESS_MESSENGER,
                    "message": "Get list vocabulary success!",
                    "list_vocabulary": [word.to_dict()
                                        for word in list_vocabulary]
                }
                return handle_before_response(response)
            else:
                return handle_before_response({"message": "Get list vocabulary failed!!"}), 202
    except Exception as ex:
        print("Error: %s" % (str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500


@bp_question_toeic.route('/update_result', methods=['POST'])
def update_result():
    try:
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if (not data) or ('username' not in data) or ("result" not in data) or ("set_question_id" not in data):
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
