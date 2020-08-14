from os import getenv
from datetime import timedelta


class BasicConfig:
    HOST = getenv('HOST', '127.0.0.1')
    PORT = int(getenv('PORT', 8000))
    SECRET_KEY = getenv('SECRET_KEY', 'secretkey')
    DEFAULT_SOCKETIO_NAMESPACE = '/messages'
    SQLALCHEMY_DATABASE_URI = getenv('DB_URI')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    DEBUG = True
    DEBUG_CELERY = True

    # Celery
    BROKER_URL = getenv('RABBIT_MQ_URL')
    CELERY_ENABLE_UTC = True
    CELERY_IMPORTS = ('backend.tasks',)
    CELERY_RESULT_BACKEND = f'db+{SQLALCHEMY_DATABASE_URI}'
    CELERY_TRACK_STARTED = True
