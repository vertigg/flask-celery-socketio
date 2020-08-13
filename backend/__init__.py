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

logging.basicConfig()

template_dir = os.path.abspath('frontend/build')
static_dir = os.path.join(template_dir, 'static')


def create_app(config_object: object = None) -> (Flask, SocketIO):
    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    if not config_object:
        logging.warn('No configuration specified, defaulting to basic config')
        app.config.from_object(BasicConfig)

    # Create SocketIO instance, using same messageq queue as Celery
    socketio = SocketIO(
        app, message_queue=app.config['BROKER_URL'], cors_allowed_origins='*'
    )
    app.socketio = socketio

    # CORS setup for regular routes
    CORS(app)

    # Register all routes
    app.register_blueprint(basic_routes)

    # Calm down socket.io loggers
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    return app, socketio


app, socketio = create_app()
