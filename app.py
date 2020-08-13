"""
Entrypoint for Flask and Celery applications
"""
from backend import app, socketio
from backend.celery_app import configure_celery
from backend.socket import TaskMessageNamespace

socketio.on_namespace(TaskMessageNamespace('/sio'))
celery = configure_celery(app)
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return {
        'celery': celery,
        'app': app,
        'socketio': socketio
    }
