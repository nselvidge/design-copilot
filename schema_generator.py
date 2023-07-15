import base64
import os
import zipfile
from io import BytesIO
from urllib.parse import urlparse
from urllib.request import urlopen
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
from ghapi.all import GhApi

load_dotenv(".env")
GH_TOKEN = os.getenv("GH_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def zipfile_from_github(repo_url, main_branch="master"):
    folder_prefix, zip_url = compute_prefix_and_zip_url(repo_url, main_branch)
    http_response = urlopen(zip_url)
    zf = BytesIO(http_response.read())
    return zipfile.ZipFile(zf, "r"), folder_prefix


def compute_prefix_and_zip_url(repo_url, main_branch="master"):
    parsed = urlparse(repo_url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("Invalid URL: " + repo_url)

    path_parts = parsed.path.strip("/").split("/")
    repo_name = path_parts[-1]
    if not repo_name:
        raise ValueError("Invalid repository URL: " + repo_url)

    folder_prefix = f"{repo_name}-{main_branch}"

    # Ensure that the URL is a GitHub repository URL
    if parsed.netloc != "github.com":
        raise ValueError("Invalid GitHub repository URL")

    # Extract the username and repository name
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    username = path_parts[0]
    repo = path_parts[1]

    # Construct the .zip file URL
    zip_url = (
        f"https://github.com/{username}/{repo}/archive/refs/heads/{main_branch}.zip"
    )

    return folder_prefix, zip_url


def list_files_in_models_folder(repo_url):
    zip_file, folder_prefix = zipfile_from_github(repo_url)
    print(folder_prefix)

    model_files = []

    for file in zip_file.namelist():
        # Check if the file is in the "models" folder
        if (
            file.startswith(f"{folder_prefix}/app/models")
            and not file.endswith("/")
            and not os.path.basename(file).startswith(".")
        ):
            model_files.append(file)

    return model_files


def generate_json_from_models(repo_url, model_files):
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo-16k-0613", temperature=0.2
    )
    for file in model_files:
        file_content = get_file_content(repo_url, file)
        prompt = PromptTemplate(
            template="""
            Convert below model into a JSON format that give the entire context of the models. Do not include any text before or after the JSON.
            Here is the model: {file_content}
            """, 
            input_variables=file_content
        )
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        print(llm_chain.run(file_content))


def get_file_content(repo_url, file_path):
    api = GhApi(token=GH_TOKEN)

    path_parts = urlparse(repo_url).path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    username = path_parts[0]
    repo = path_parts[1]

    # This will remove 'rails-realworld-example-app-master/' from the file_path
    relative_file_path = file_path.replace(f"{repo}-master/", "")

    try:
        commits = api.repos.list_commits(username, repo, path=relative_file_path)
    except Exception as e:
        print(f"Failed to get commits for file: {relative_file_path}")
        print(f"Error: {e}")
        return None

    if commits:
        latest_commit_sha = commits[0].sha
        try:
            file_content = api.repos.get_content(
                username, repo, path=relative_file_path, ref=latest_commit_sha
            )
            decoded_content = base64.b64decode(file_content.content).decode("utf-8")
            num_lines = len(decoded_content.splitlines())

            # Check if the file is too large
            if num_lines > 1000:
                print(f"File {relative_file_path} is too large, skipping...")
                return None

            return decoded_content
        except Exception as e:
            print(f"Failed to get file content for file: {relative_file_path}")
            print(f"Error: {e}")
    else:
        print(f"No commits found for file: {relative_file_path}")

    return None


if __name__ == "__main__":
    repo_url = "https://github.com/gothinkster/rails-realworld-example-app"
    model_files = list_files_in_models_folder(repo_url)
    generate_json_from_models(repo_url, model_files)

    # print(file_content)
