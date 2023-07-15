import schema_generator
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask("design-copilot")
cors = CORS(app)


@app.route("/v1/generate_schema", methods=["POST"])
@cross_origin()
def generate_schema():
    req_data = request.get_json()
    branch_name = req_data["branch_name"]
    repo_url = req_data["repo_url"]

    try:
        model_files = schema_generator.list_files_in_models_folder(repo_url, branch_name)
        print("REEEEEE:", model_files)
        schema_generator.generate_json_from_models(repo_url, branch_name, model_files)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(message="JSON file was saved as output.json"), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
