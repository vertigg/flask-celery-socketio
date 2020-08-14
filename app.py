"""
Entrypoint for Flask and Celery applications
"""
from backend import create_app, create_socket_io
from backend.celery_app import configure_celery
from backend.socket import TaskMessageNamespace
from backend.database import db

app = create_app()
socketio = create_socket_io(app)
celery = configure_celery(app, socketio)
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return {
        'celery': celery,
        'app': app,
        'socketio': socketio,
        'db': db
    }
