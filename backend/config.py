from os import getenv


class BasicConfig:
    DB_URI = None
    HOST = getenv('HOST', '127.0.0.1')
    PORT = int(getenv('PORT', 8000))
    SECRET_KEY = getenv('SECRET_KEY', 'secretkey')

    DEBUG = True
    DEBUG_CELERY = True

    # Celery
    BROKER_URL = getenv('RABBIT_MQ_URL')
    CELERY_ENABLE_UTC = True
    CELERY_IMPORTS = ('backend.tasks',)
    CELERY_RESULT_BACKEND = 'rpc'
    CELERY_TRACK_STARTED = True
