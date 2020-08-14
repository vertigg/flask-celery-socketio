"""
Flask and SocketIO initialization and configuration
"""
import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from backend.config import BasicConfig
from backend.routes import basic_routes
from backend.socket import TaskMessageNamespace
from backend.database import db

logging.basicConfig()

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')


def create_app(config_object: object = None) -> Flask:
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    if not config_object:
        logging.warn('No configuration specified, defaulting to basic config')
        app.config.from_object(BasicConfig)

    # Register all routes and setup CORS
    app.register_blueprint(basic_routes)
    CORS(app)

    # Initialize db
    db.init_app(app)
    db.app = app

    return app


def create_socket_io(app: Flask) -> SocketIO:
    # Create SocketIO instance, using same messageq queue as Celery
    socketio = SocketIO(
        app,
        message_queue=app.config['BROKER_URL'],
        cors_allowed_origins='*'
    )
    app.socketio = socketio

    # Calm down socket.io loggers
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    # Register namespaces and listeners
    default_namespace = TaskMessageNamespace(app.config['DEFAULT_SOCKETIO_NAMESPACE'])
    socketio.on_namespace(default_namespace)

    return socketio
