from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
from entity.user import User
import json
import os
import util
import time
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = util.sha256_encode(os.getenv("SECRET_KEY"))
SUCCESS_MESSENGER = "sucsess"

#token black list
token_blacklist = set()

# Function to generate a JWT token
def generate_token(user):
    payload = {
        'username': user.getUsername(),
        "password": user.getPassword(),
        'exp': datetime.utcnow() + timedelta(seconds=30)  # Token expiration time
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
        return jsonify({'message': 'Logout successful'})

    else:
        return jsonify({'error': verification_result}), 401

@app.route("/",methods=['GET'])
def home():
    response = {
        "status": SUCCESS_MESSENGER,
        "messenger": "WELLCOME HOME!!"
    }
    return jsonify(response)

def checkdatabase(user):
    with open("data.json", 'r') as file:
        list_user = json.load(file)
        matching_users = filter(lambda item: item['username'] == user.getUsername() and item['password'] == user.getPassword(), list_user)
        # Check if there's at least one matching user
        return any(matching_users)
    
# Route for token generation
@app.route('/login', methods=['POST'])
def login():
    user = User()
    if request.form:
        data = request.form
    elif request.is_json:
        data = request.get_json()
    else:
        return jsonify({'error': 'Invalid data format'}), 400
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 401
    else:
        user.setPassword(data.get('password'))
        user.setUsername(data.get('username'))
        if checkdatabase(user):

            # In a real application, validate the username and password against a database
            # For simplicity, let's assume any username/password combination is valid
            token = generate_token(user)
            response = {
                'token': token,
                "status": SUCCESS_MESSENGER,
                "message": "Success login with %s"%(user.getUsername())
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'Invalid credentials/Wrong username:password'}), 401

# Route for protected resource
@app.route('/protected', methods=['POST'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    
    verification_result = verify_token(token)
    if 'username' in verification_result:
        return jsonify({'message': 'Access granted!'})
    else:
        return jsonify({'error': verification_result}), 401

# Route for logout (blacklisting token)
@app.route('/logout', methods=['POST'])
def user_logout():
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'Token is missing'}), 400


    return logout(token)

# Event to signal the thread to exit
exit_event = Event()

# Function to periodically clean up expired tokens
def clean_expired_tokens():
    while not exit_event.is_set():
        print("Running remove auto token black list.....")
        time.sleep(30)  # Sleep for 30 seconds
        now = datetime.utcnow()
        expired_tokens = {token for token in token_blacklist if 'exp' not in verify_token(token)}
        token_blacklist.difference_update(expired_tokens)
        print("Remove: %s"%(str(expired_tokens)))

# Start the clean-up thread
cleanup_thread = Thread(target=clean_expired_tokens)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
    
# Wait for the thread to finish before exiting the application
exit_event.set()
cleanup_thread.join()
