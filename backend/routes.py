from flask import Blueprint, abort, jsonify, render_template, request

from backend.tasks import long_task

basic_routes = Blueprint('simple_page', __name__)


@basic_routes.route('/', methods=('get',))
def index():
    return render_template('index.html')


@basic_routes.route('/start_task', methods=('POST',))
def start_simple_task(*args, **kwargs):
    """Starts simple Celery task on post request and returns task ID"""
    if request.method == 'POST':
        data = request.json
        task = long_task.delay(room=data.get('requestSid'))
        return jsonify({'message': f'Celery task has been launched with id {task.id}'})
    abort(404)
