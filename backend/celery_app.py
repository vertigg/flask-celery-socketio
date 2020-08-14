"""
Celery initialization and configuration
"""
from celery import Celery
from flask import Flask
from flask_socketio import SocketIO

celery = Celery(__name__, backend='rpc://')


def configure_celery(app: Flask, socketio: SocketIO) -> Celery:
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
                self._socketio = socketio
            return self._socketio

        def emit_response(self, message, room, event_type='response', namespace=None):
            if not namespace:
                namespace = app.config['DEFAULT_SOCKETIO_NAMESPACE']
            self.socketio.emit(
                event_type, {'message': message}, room=room, namespace=namespace
            )

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextAwareTask

    celery.finalize()
    return celery
