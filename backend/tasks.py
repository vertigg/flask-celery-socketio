import time

import requests
from flask import request

from backend.celery_app import celery


@celery.task(bind=True)
def long_task(self, room: str):
    r = requests.get('https://httpbin.org/delay/5')
    self.emit_response(f'Task finished with status code {r.status_code}', room)
    return r.status_code


@celery.task(bind=True)
def message_to_client(self, message, room):
    self.emit_response(message, room)
