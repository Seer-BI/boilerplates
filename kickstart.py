def create_git_repo(folder_path, repo_name, access_token):
    # Create a new repository on GitHub
    repo_url = f"https://api.github.com/orgs/Seer-BI/repos"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": repo_name,
        "private": True
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


def get_base_folder(filepath):
    # If folder location is explicitly specified, use it
    # otherwise, use the default "Projects" folder located inthe user's home directory
    home_folder = os.path.expanduser("~")
    projects_folder = os.path.join(home_folder, "Projects")
    
    # Create "Projects" folder if it doesn't exist
    if not os.path.exists(projects_folder):
        os.makedirs(projects_folder)
    
    absolute_path = os.path.join(projects_folder, filepath)
    
    basename = os.path.basename(absolute_path.rstrip('/'))
    folder_path = os.path.dirname(absolute_path)
    
    if not basename:
        return get_base_folder(folder_path)
    else:
        return basename, folder_path


def fetch_online(url, output_file):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Write the response content to the output file
        with open(output_file, 'wb') as file:
            file.write(response.content)


def install_library(library_name):
    try:
        if library_name == "GitPython":
            __import__("git")
        else:
            __import__(library_name)
        print(f"{library_name} library is already installed.")
    except ImportError:
        print(f"{library_name} library is not installed. Installing it now...")
        try:
            subprocess.run(["pip", "install", library_name], check=True)
            print(f"{library_name} library has been successfully installed. Please run the script again.")
            exit(0)
        except subprocess.CalledProcessError:
            print(f"Failed to install {library_name} library. Please install it manually.")




if __name__ == "__main__":
    import os
    import subprocess
    import argparse
    
    # Install GitPython if not already installed
    install_library("GitPython")
    # Install requests if not already installed
    install_library("requests")
    
    import git
    import requests
            
    access_token = os.environ.get("GIT_ACCESS_TOKEN")
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Create a new Work Directory')

    # Add an argument to the parser
    parser.add_argument('--job-path', help='Path to the folder')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the variable values
    project_path = args.job_path
    
    workflow_name, base_path = get_base_folder(project_path)
    
    project_path = os.path.join(base_path, workflow_name)
    
    print("Creating a new Work Directory at {}...".format(project_path))
    
    # Create the project directory
    try:
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        else:
            print("The project directory already exists.")
            exit(1)
    except OSError as error:
        print(error, "Failed to create the project directory.")

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
            "artifacts": {
                "data": [],
                "models": [],
                "reports": []
            },
            "scripts": [
                "app.py"
            ],
            "test": ""  # Added a value for the "test" file
        }
    }

    # Create the directory structure starting from the base_path
    create_directory_structure(base_path, folders)

    # Download the README.md file from the GitHub repository
    readme_url = "https://raw.githubusercontent.com/Seer-BI/boilerplates/main/README_template.md"
    readme_output_file = os.path.join(project_path, "README.md")
    fetch_online(readme_url, readme_output_file)

    # Download the logo from the GitHub repository
    logo_url = "https://github.com/Seer-BI/boilerplates/blob/main/media/company_logo.png"
    logo_output_file = os.path.join(project_path, "media", "company_logo.png")
    fetch_online(logo_url, logo_output_file)

    # Download the .gitignore file from the GitHub repository
    gitignore_url = "https://raw.githubusercontent.com/Seer-BI/boilerplates/main/.gitignore"
    gitignore_output_file = os.path.join(project_path, ".gitignore")
    fetch_online(gitignore_url, gitignore_output_file)

    # Send to GitHub
    create_git_repo(base_path, workflow_name, access_token)


    # python -u "c:\Users\Chukwudi Ajoku\Project\SeerBI Utilities\kickstart.py" --job-path "c:\Users\Chukwudi Ajoku\Project\Playplay"


# How to set up if you want it easier, run as cmd as admin:
# 1. copy "path\to\kickstart.py" "c:\" (or wherever safer you want it)
# 2. notepad $PROFILE
# 3. add this line to the file: function kickstart {python -u "c:\kickstart.py" --job-path $args[0]}
# 4. save and close
# 5. restart powershell
# 6. run "kickstart Folder"
# Folder is a folder name or path.

# A folder called "Projects" must exist in your home directory. where it does not exist, it will be created.

# Note: You may need to enable script execution in PowerShell. You can do this by opening an elevated PowerShell session (Run as Administrator) and running the following command:
# Set-ExecutionPolicy RemoteSigned
