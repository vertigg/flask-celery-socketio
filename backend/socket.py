from flask import request, session
from flask_socketio import Namespace, emit, join_room, leave_room

from backend.tasks import long_task, message_to_client


class TaskMessageNamespace(Namespace):
    def on_connection(self, *args):
        sid = session.get('sid')
        join_room(sid)
        emit('confirmation', {
            'message': (
                f'Connected to a Flask, SocketIO, using unique ID: {sid} '
            )})

    def on_disconnect(self):
        sid = session.get('sid')
        leave_room(sid)
