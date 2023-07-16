import os
import json
import uuid

import redis
from celery import Celery
from dotenv import load_dotenv

import schema_generator
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask("app")
cors = CORS(app)

load_dotenv('server/.env')
CLOUDAMQP_URL = os.getenv("CLOUDAMQP_URL", "")
REDIS_URL = os.getenv("REDIS_URL", "")
GH_TOKEN = os.getenv("GH_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
print(OPENAI_API_KEY)

# Initialize Celery
celery = Celery(
    app.name,
    broker=CLOUDAMQP_URL,
    backend=REDIS_URL,
)

r = redis.Redis(host='localhost', port=6379, db=0)


@celery.task
def generate_json_from_models_task(req_data, random_uuid):
    branch_name = req_data["branch_name"]
    repo_url = req_data["repo_url"]

    try:
        print("Generating JSON from models...")
        model_files = schema_generator.list_files_in_models_folder(
            repo_url, branch_name)
        json_model_dict = schema_generator.generate_json_from_models(
            repo_url, branch_name, model_files, random_uuid)
    except Exception as e:
        return {'error': str(e)}

    return json_model_dict


@app.route("/v1/generate_schema", methods=["POST"])
@cross_origin()
def generate_schema():
    print("Generating schema")
    req_data = request.get_json()
    try:
        print("Starting task...")
        random_uuid = uuid.uuid4()
        task = generate_json_from_models_task.delay(req_data, random_uuid)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(id=random_uuid), 200


@app.route("/v1/task/<task_id>", methods=["GET"])
@cross_origin()
def get_task_result(task_id):
    filename = f"server/{task_id}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            result = json.load(file)
        response = {
            'state': 'SUCCESS',
            'result': result,
        }
    else:
        response = {
            'state': 'PENDING',
            'status': 'Task is still running or the file does not exist...',
        }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
