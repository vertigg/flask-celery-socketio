from celery.exceptions import TimeoutError
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


@basic_routes.route('/result/<task_id>')
def result(task_id):
    try:
        task = long_task.AsyncResult(task_id)
        result = task.get(timeout=5)
        response = {
            'state': task.state,
            'status_code': result,
        }
        return jsonify(response)
    except TimeoutError:
        return jsonify({
            'error': {'message': f'Can not found task with id: {task_id}'}
        })
