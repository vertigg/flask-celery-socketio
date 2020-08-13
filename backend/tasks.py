import time

import requests
from flask import request

from backend.celery_app import celery


@celery.task(bind=True)
def long_task(self, room: str):
    r = requests.get('https://httpbin.org/delay/5')
    self.socketio.emit(
        'response',
        {'message': f'Task finished with status code {r.status_code}'},
        namespace='/sio',
        room=room
    )
    return r.status_code


@celery.task(bind=True)
def message_to_client(self, message, room):
    self.socketio.emit('response', {'data': message}, namespace='/sio', room=room)
