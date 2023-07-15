import os
import zipfile
from io import BytesIO
from urllib.parse import urlparse
from urllib.request import urlopen


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
        if file.startswith(f"{folder_prefix}/app/models") and not file.endswith('/') and not os.path.basename(file).startswith('.'):
            model_files.append(file)

    return model_files


if __name__ == "__main__":
    # Example usage:
    repo_url = "https://github.com/gothinkster/rails-realworld-example-app"
    print(list_files_in_models_folder(repo_url))
