from flask import request
from flask_socketio import Namespace, emit, join_room, leave_room

from backend.tasks import long_task, message_to_client


class TaskMessageNamespace(Namespace):
    def on_connection(self, *args):
        join_room(request.sid)
        emit('confirmation', {
            'requestSid': request.sid,
            'message': f'Connected to a Flask, SocketIO, using unique ID: {request.sid}'
        })

    def on_disconnect(self):
        leave_room(request.sid)
