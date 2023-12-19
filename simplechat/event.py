from flask_socketio import emit#, join_room, leave_room
from app import socketio
from flask import session


@socketio.on('chat_simple', namespace='/chat/simple')
def handle_message(message):
    emit('chat', message, broadcast=True)


@socketio.on('joined', namespace='/chat/simple')
def joined(message):
    # room = session.get('room')
    # join_room(room)
    emit('chat', session.get('name','') + ' has entered the room.', broadcast=True)



@socketio.on('left', namespace='/chat/simple')
def left(message):
    # room = session.get('room')
    #leave_room(room)
    emit('chat', session.get('name','') + ' has left the room.', broadcast=True)