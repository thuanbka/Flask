
from flask import Flask
from my_app import create_app, socketio

# server = Flask(__name__)
# server.wsgi_app = create_app()
if __name__ == '__main__':
    # #Create a app
    server = Flask(__name__)
    server.wsgi_app = create_app()
    # server.run(debug=True, port=server.wsgi_app.config["PORT"], host=server.wsgi_app.config["HOST_NAME"])
    # socketio.run(server, debug=True, port=server.wsgi_app.config["PORT"], host=server.wsgi_app.config["HOST_NAME"], allow_unsafe_werkzeug=True)
    socketio.run(server, debug=True, port=server.wsgi_app.config["PORT"], host=server.wsgi_app.config["HOST_NAME"])

