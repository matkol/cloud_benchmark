#!/usr/bin/env python

import os
import time
from flask import Flask, request, jsonify, current_app, g as app_ctx

from app.tasks import long_running_task
from app.tasks import add
from app.utils import download_blob


app = Flask(__name__)

# Configure Celery with RabbitMQ
# app.config['CELERY_BROKER_URL'] = os.environ.get("CELERY_BROKER_URL", "amqp://guest@localhost//")
# Configure Celery with Redis
app.config['CELERY_BROKER_URL'] = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.config['CELERY_RESULT_BACKEND'] = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


health_status = True


# Some Flasky way to measure the timing for each endpoint
########################################################################################################################
@app.before_request
def _before():
    # Store the start time for the request
    app_ctx.start_time = time.perf_counter()


@app.after_request
def _after(response):
    # Get total time in milliseconds
    total_time = time.perf_counter() - app_ctx.start_time
    time_in_ms = int(total_time * 1000)
    # Log the time taken for the endpoint
    current_app.logger.info('%s ms %s %s %s', time_in_ms, request.method, request.path, dict(request.args))
    return response
########################################################################################################################


# Flask API endpoints
########################################################################################################################
@app.route('/add', methods=['POST'])
def start_add():
    app.logger.info(request.json)
    request.json.pop("duration")
    task = add.delay(args=[request.json['x'], request.json['y']])
    return jsonify({"task_id": task.id}), 202


@app.route('/task', methods=['POST'])
def start_task():
    app.logger.info(request.json)
    duration = request.json.get('duration', 5)
    task = long_running_task.apply_async(args=[duration], kwargs=request.json)
    return jsonify({"task_id": task.id}), 202


# Get task result API endpoint
@app.route('/task-result/<string:task_id>', methods=['GET'])
def task_result(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"status": "PENDING"}
    elif task.state == 'SUCCESS':
        response = {"status": "SUCCESS", "result": task.result}
    else:
        response = {"status": "FAILURE"}

    return jsonify(response)


@app.route("/load", methods=['GET', 'POST'])
def load():
    print("Downloading...")
    if request.method == 'POST':
        data = request.json
        app.logger.info(data)
        download_blob(data['bucket'], data['blob_name'], data['local_name'])
        return jsonify(data)
    else:
        download_blob("download-test-data", "10mb-001", "10mb-001")
        return "<p>Hello, World!</p>"


@app.route("/health")
def health():
    if health_status:
        resp = jsonify(health="healthy")
        resp.status_code = 200
    else:
        resp = jsonify(health="unhealthy")
        resp.status_code = 500
    return resp
########################################################################################################################


if __name__ == "__main__":
    app.run(debug=True)
