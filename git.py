import requests
from crewai_tools import tool
import json
import base64

class GitHubOperations:
    def __init__(self, username, access_token):
        self.username = username
        self.access_token = access_token

    def create_repository_and_issue(self, repo_name, description="", issue_title=None, issue_body=""):
        # Create repository
        url_repo = f"https://api.github.com/user/repos"
        payload_repo = json.dumps({
            "name": repo_name,
            "description": description,
            "private": False
        })
        headers_repo = {
            'Authorization': f'token {self.access_token}',
            'Content-Type': 'application/json'
        }
        response_repo = requests.post(url_repo, headers=headers_repo, data=payload_repo)

        if response_repo.status_code != 201:
            raise Exception(f"Failed to create repository: {response_repo.json()}")

        print(f"Repository '{repo_name}' created successfully.")

        # Create issue if issue_title is provided
        if issue_title:
            url_issue = f"https://api.github.com/repos/{self.username}/{repo_name}/issues"
            payload_issue = json.dumps({
                "title": issue_title,
                "body": issue_body
            })
            headers_issue = {
                'Authorization': f'token {self.access_token}',
                'Content-Type': 'application/json'
            }
            response_issue = requests.post(url_issue, headers=headers_issue, data=payload_issue)

            if response_issue.status_code != 201:
                raise Exception(f"Failed to create issue: {response_issue.json()}")

            print(f"Issue '{issue_title}' created successfully in '{repo_name}'.")

        return f"Repository '{repo_name}' created successfully."

    def create_initial_commit(self, repo_name):
        url_file = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/README.md"
        payload_file = json.dumps({
            "message": "Initial commit",
            "content": base64.b64encode(b"# Initial Commit").decode(),
            "branch": "main"
        })
        headers_file = {
            'Authorization': f'token {self.access_token}',
            'Content-Type': 'application/json'
        }
        response_file = requests.put(url_file, headers=headers_file, data=payload_file)

        if response_file.status_code != 201:
            raise Exception(f"Failed to create initial commit in branch 'main': {response_file.json()}")

        print("Initial commit created successfully in branch 'main'.")

    def create_branch(self, repo_name, branch_name, base_branch="main"):
        # Get the SHA of the base branch
        url_branch = f"https://api.github.com/repos/{self.username}/{repo_name}/git/refs/heads/{base_branch}"
        headers_branch = {
            'Authorization': f'token {self.access_token}',
            'Content-Type': 'application/json'
        }
        response_branch = requests.get(url_branch, headers=headers_branch)

        if response_branch.status_code != 200:
            raise Exception(f"Failed to get base branch '{base_branch}': {response_branch.json()}")

        base_branch_sha = response_branch.json()["object"]["sha"]

        # Create the new branch
        url_create_branch = f"https://api.github.com/repos/{self.username}/{repo_name}/git/refs"
        payload_create_branch = json.dumps({
            "ref": f"refs/heads/{branch_name}",
            "sha": base_branch_sha
        })
        response_create_branch = requests.post(url_create_branch, headers=headers_branch, data=payload_create_branch)

        if response_create_branch.status_code != 201:
            raise Exception(f"Failed to create branch '{branch_name}': {response_create_branch.json()}")

        print(f"Branch '{branch_name}' created successfully from '{base_branch}'.")

    def create_file_in_branch(self, repo_name, file_name, file_content, branch_name="main"):
        url_file = f"https://api.github.com/repos/{self.username}/{repo_name}/contents/{file_name}"
        payload_file = json.dumps({
            "message": f"Add {file_name}",
            "content": base64.b64encode(file_content.encode()).decode(),
            "branch": branch_name
        })
        headers_file = {
            'Authorization': f'token {self.access_token}',
            'Content-Type': 'application/json'
        }
        response_file = requests.put(url_file, headers=headers_file, data=payload_file)

        if response_file.status_code != 201:
            raise Exception(f"Failed to create file '{file_name}' in branch '{branch_name}': {response_file.json()}")

        print(f"File '{file_name}' created successfully in branch '{branch_name}'.")

@tool
def github_operations(repo_name, description="", issue_title=None, issue_body="", feature_branch="feature", file_name=None, file_content=None):
    """
    Create a new repository on GitHub, optionally add an issue, create a feature branch, and add a file.

    Args:
    - repo_name (str): The name of the repository to create.
    - description (str, optional): The description of the repository.
    - issue_title (str, optional): Title of the issue to create.
    - issue_body (str, optional): Body/content of the issue.
    - feature_branch (str, optional): Name of the feature branch to create.
    - file_name (str, optional): Name of the file to add.
    - file_content (str, optional): Content of the file to add.

    Returns:
    - str: Success or error message.

    Raises:
    - Exception: If there is an error creating the repository, issue, branch, or file.

    Usage:
    This tool creates a new repository on GitHub, optionally adds an issue, creates a feature branch, and adds a file.
    """
    username = "Akashv0907"
    access_token = "GITHUB_TOKEN"

    github_ops = GitHubOperations(username, access_token)
    result_message = github_ops.create_repository_and_issue(repo_name, description, issue_title, issue_body)

    try:
        github_ops.create_initial_commit(repo_name)
        github_ops.create_branch(repo_name, feature_branch)
        result_message += f" Branch '{feature_branch}' created successfully."
    except Exception as e:
        result_message += f" Error creating branch '{feature_branch}': {str(e)}"

    if file_name and file_content:
        try:
            github_ops.create_file_in_branch(repo_name, file_name, file_content, feature_branch)
            result_message += f" File '{file_name}' created successfully in branch '{feature_branch}'."
        except Exception as e:
            result_message += f" Error creating file '{file_name}' in branch '{feature_branch}': {str(e)}"

    return result_message
