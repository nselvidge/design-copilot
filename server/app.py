import os
import json
import redis
from celery import Celery
from dotenv import load_dotenv

import schema_generator
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask("design-copilot")
cors = CORS(app)

load_dotenv('server/.env')
CLOUDAMQP_URL = os.getenv("CLOUDAMQP_URL", "")
REDIS_URL = os.getenv("REDIS_URL", "")

# Initialize Celery
celery = Celery(
    app.name,
    broker=CLOUDAMQP_URL,
    backend=REDIS_URL,
)


@celery.task
def generate_json_from_models_task(req_data):
    branch_name = req_data["branch_name"]
    repo_url = req_data["repo_url"]

    try:
        print("Generating JSON from models...")
        model_files = schema_generator.list_files_in_models_folder(repo_url, branch_name)
        json_model_dict = schema_generator.generate_json_from_models(repo_url, branch_name, model_files)
    except Exception as e:
        return {'error': str(e)}

    return json_model_dict


@app.route("/v1/generate_schema", methods=["POST"])
@cross_origin()
def generate_schema():
    req_data = request.get_json()
    try:
        print("Starting task...")
        task = generate_json_from_models_task.delay(req_data)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(task_id=task.id), 200


@app.route("/v1/task/<task_id>", methods=["GET"])
@cross_origin()
def get_task_result(task_id):
    result = r.get(task_id)
    if result is None:
        response = {
            'state': 'PENDING',
            'status': 'Task is still running...'
        }
    else:
        result = json.loads(result)
        if 'error' in result:
            response = {
                'state': 'FAILURE',
                'error': result['error'],
            }
        else:
            response = {
                'state': 'SUCCESS',
                'result': result,
            }
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
