def create_git_repo(folder_path, repo_name, access_token):
    # Create a new repository on GitHub
    repo_url = f"https://api.github.com/orgs/Seer-BI/repos"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": repo_name
    }
    response = requests.post(repo_url, json=payload, headers=headers)
    print(response.status_code)
    if response.status_code != 201:
        print("Failed to create repository. Check your access token and organisation.")
        return

    # Get the created repository's URL
    repo_info = response.json()
    repo_git_url = repo_info.get("clone_url")

    # Initialize a new Git repository in the local folder
    repo = git.Repo.init(f"{folder_path}/{repo_name}")
    repo.create_remote("origin", repo_git_url)

    # Add all files in the folder to the Git repository
    repo.git.add(all=True)

    # Commit the changes
    repo.git.commit("-m", "Initial commit")

    # Push the changes to the remote repository
    repo.git.push("--set-upstream", "origin", "master")

    print("Successfully created and pushed to the repository.")

    

# Helper function to create directories, subdirectories, and files recursively
def create_directory_structure(directory, folders_dict):
    for folder, content in folders_dict.items():
        path = os.path.join(directory, folder)
        os.makedirs(path, exist_ok=True)

        if isinstance(content, list):
            for file in content:
                file_path = os.path.join(path, file)
                open(file_path, 'a').close()  # Create an empty file
        elif isinstance(content, dict):
            create_directory_structure(path, content)


def fetch_online(url, output_file):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Write the response content to the output file
        with open(output_file, 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    import os
    import requests
    import subprocess
    import argparse
    # Install GitPython if not already installed
    try:
        import git
        print("GitPython is already installed.")
    except ImportError:
        try:
            # Install GitPython using pip
            subprocess.run(["pip", "install", "GitPython"], check=True)
            import git
            print("GitPython has been successfully installed.")
        except subprocess.CalledProcessError:
            print("Failed to install GitPython. Please install it manually.")
    
    base_path = "./"
    access_token = os.environ.get("GIT_ACCESS_TOKEN")
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Create a new Work Directory')

    # Add an argument to the parser
    parser.add_argument('--job', help='Path to the folder')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the variable values
    workflow_name = args.job
    
    print(workflow_name)

    folders = {
        workflow_name: {
            "tools": [],
            "notebooks": [
                "data_exploration.ipynb",
                "data_processing.ipynb",
                "model_training.ipynb",
                "model_evaluation.ipynb",
                "model_deployment.ipynb"
            ],
            "media": [],
            "artifacts": [
                "data",
                "models",
                "reports"
            ],
            "scripts": [
                "app.py"
            ],
            "test": ""  # Added a value for the "test" file
        }
    }

    # Create the directory structure starting from the base_path
    create_directory_structure(base_path, folders)

    # Download the README.md file from the GitHub repository
    readme_url = "https://raw.githubusercontent.com/Seer-BI/boilerplates/main/README.md"
    readme_output_file = "./{}/README.md".format(workflow_name)
    fetch_online(readme_url, readme_output_file)

    # Download the logo from the GitHub repository
    logo_url = "https://github.com/Seer-BI/boilerplates/blob/main/media/company_logo.png"
    logo_output_file = "./{}/media/company_logo.png".format(workflow_name)
    fetch_online(logo_url, logo_output_file)

    # Download the .gitignore file from the GitHub repository
    gitignore_url = "https://raw.githubusercontent.com/Seer-BI/boilerplates/main/.gitignore"
    gitignore_output_file = "./{}/.gitignore".format(workflow_name)
    fetch_online(gitignore_url, gitignore_output_file)

    # Send to GitHub
    create_git_repo(base_path, workflow_name, access_token)
