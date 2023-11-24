from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import jwt
from datetime import datetime, timedelta
from entity.user import User
import json
from utils import util
import time
from threading import Thread, Event
import typing as t
from flask import current_app as app

bp_dashboard = Blueprint("dashboard", __name__, template_folder="templates")
SUCCESS_MESSENGER = "sucsess"
EXPIRED_TIME = 3600
#token black list
token_blacklist = set()

# Function to generate a JWT token
def generate_token(user):
    payload = {
        'username': user.getUsername(),
        'password': user.getPassword(),
        'role': user.getRole(),
        'exp': datetime.utcnow() + timedelta(seconds=EXPIRED_TIME)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Function to verify a JWT token
def verify_token(token):
    try:
        # Check if the token is in the blacklist
        if token in token_blacklist:
            raise jwt.InvalidTokenError('Token has been blacklisted')

        decoded_payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return 'Token has expired'
    except jwt.InvalidTokenError as e:
        print(f'Invalid token: {str(e)}')
        return f'Invalid token: {str(e)}'

# Function to logout (add token to the blacklist)
def logout(token):
    verification_result = verify_token(token)
    if 'username' in verification_result:
        token_blacklist.add(token)
        print(f'Token {token} has been blacklisted')
        return handle_before_response({'message': 'Logout successful'})

    else:
        return handle_before_response({'error': verification_result}), 401

@bp_dashboard.route("/",methods=['GET'])
def home():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "WELLCOME HOME!!",
        "view": "home.html"
    }
    return handle_before_response(response)

@bp_dashboard.route("/login",methods=['GET'])
def get_login():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "Please login!!",
        "view": "login.html"
    }
    return handle_before_response(response)

def checkdatabase(user):
    with open("data.json", 'r') as file:
        list_user = json.load(file)
        matching_users = list(filter(lambda item: item['username'] == user.getUsername() and item['password'] == user.getPassword(), list_user))
        # Check if there's at least one matching user
        if len(matching_users) >= 1:
            user = User(**matching_users[0])
            return user
        return None
    
# Route for token generation
@bp_dashboard.route('/login', methods=['POST'])
def login():
    try:
        SUPPORT_FRONT_END = app.config["SUPPORT_FRONT_END"]
        if request.form:
            data = request.form
        elif request.is_json:
            data = request.get_json()
        else:
            return handle_before_response({'error': 'Invalid data format'}), 400

        if not data or 'username' not in data or 'password' not in data:
            return handle_before_response({'error': 'Invalid data'}), 401
        else:
            password = util.sha256_encode(data.get('password'))
            username = data.get('username')
            user = User(username=username, password=password)
            user = checkdatabase(user)
            if user != None:
                # In a real application, validate the username and password against a database
                # For simplicity, let's assume any username/password combination is valid
                token = generate_token(user)
                response = {
                    "token": token,
                    "status": SUCCESS_MESSENGER,
                    "message": "Success login with %s and role %s"%(user.getUsername(), user.getRole()),
                    "user_name": user.username
                }
                if SUPPORT_FRONT_END:
                    return redirect(url_for('dashboard.welcome', response = json.dumps(response)))
                else:
                    return handle_before_response(response)
            else:
                return handle_before_response({'error': 'Invalid credentials/Wrong username:password'}), 401
    except Exception as ex:
        print("Error: %s"%(str(ex)))
        return handle_before_response({'error': 'Have error from server'}), 500

# Router for welcome resource
@bp_dashboard.route('/welcome', methods=["GET"])
def welcome():
    response = {
        "status": SUCCESS_MESSENGER,
        "message": "WELCOME to WELCOME",
    }
    if "response" in request.args:
        response = json.loads(request.args.get("response"))
    user = User()
    if response != None and "user_name" in response:
        user.setUsername(response["user_name"])
        del response["user_name"]
    else:
        user.setUsername("Noname_user")
    response["view"] = "welcome.html"
    return handle_before_response(response,user=user)

# Route for protected resource
@bp_dashboard.route('/protected', methods=['POST'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return handle_before_response({'error': 'Token is missing'}), 401

    verification_result = verify_token(token)
    if 'username' in verification_result:
        return handle_before_response({'message': 'Access granted!'})
    else:
        return handle_before_response({'error': verification_result}), 401

# Route for admin resource
@bp_dashboard.route('/admin', methods=['POST'])
def check_login_as_admin():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return handle_before_response({'error': 'Token is missing'}), 401

        verification_result = verify_token(token)
        if 'username' in verification_result and 'role' in verification_result and verification_result['role'] == 'admin':
            return handle_before_response({'message': 'Access as a admin granted!'})
        else:
            return handle_before_response({'error': 'You use wrong token with admin'}), 401
    except Exception as ex:
        print("Error: %s"%(str(ex)))
        return handle_before_response({'error': 'Have something wrong from server'}), 500

# Route for logout (blacklisting token)
@bp_dashboard.route('/logout', methods=['POST'])
def user_logout():
    token = request.headers.get('Authorization')
    
    if not token:
        return handle_before_response({'error': 'Token is missing'}), 400

    return logout(token)

# Event to signal the thread to exit
exit_event = Event()

# Function to periodically clean up expired tokens
def clean_expired_tokens():
    while not exit_event.is_set():
        print("Running remove auto token black list.....")
        time.sleep(EXPIRED_TIME)  # Sleep for EXPIRED_TIME seconds
        expired_tokens = {token for token in token_blacklist if 'exp' not in verify_token(token)}
        token_blacklist.difference_update(expired_tokens)
        print("Remove: %s"%(str(expired_tokens)))

# Start the clean-up thread
cleanup_thread = Thread(target=clean_expired_tokens)
#cleanup_thread.start()


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
    
# Wait for the thread to finish before exiting the application
# exit_event.set()
# cleanup_thread.join()
