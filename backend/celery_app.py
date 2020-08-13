"""
Celery initialization and configuration
"""
from celery import Celery
from flask import Flask
from flask_socketio import SocketIO

celery = Celery(__name__, backend='rpc://')


def configure_celery(app: Flask) -> Celery:
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextAwareTask(TaskBase):
        abstract = True
        _socketio = None

        @property
        def socketio(self):
            """
            Helper property that will allow Celery tasks to open SocketIO connections
            """
            if not self._socketio:
                self._socketio = SocketIO(message_queue=app.config['BROKER_URL'])
            return self._socketio

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextAwareTask

    celery.finalize()
    return celery
