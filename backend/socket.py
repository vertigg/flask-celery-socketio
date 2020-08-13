from flask import request
from flask_socketio import Namespace, emit, join_room, leave_room

from backend.tasks import long_task, message_to_client


class TaskMessageNamespace(Namespace):
    def on_connection(self, *args):
        join_room(request.sid)
        emit(
            'confirmation', {
                'connectionStatus': f'Connected to a socket, using room {request.sid}',
                'requestSid': request.sid
            }
        )

    def on_submit(self, *args):
        print(args)
        roomstr = request.sid
        join_room(roomstr)
        task = long_task.delay(room=roomstr)
        message_to_client.delay(f'Task {task.id} started', room=roomstr)

    def on_disconnect(self):
        leave_room(request.sid)
