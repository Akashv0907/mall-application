from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from tools.git import github_operations

repo_name = input("Enter the repository name: ")
description = input("Enter the repository description (optional): ")
issue_title = input("Enter the issue title: ")
issue_body = input("Enter the issue description: ")
file_name = input("Enter the file name: ")
file_content = input("Enter the file content: ")
branch_name = input("Enter the branch name: ")
pr_title = input("Enter the pull request title: ")
pr_body = input("Enter the pull request description: ")

my_llm = ChatGroq(
    api_key="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",
    model="llama3-8b-8192",
)

ScrumMaster = Agent(
    role="Scrum Master",
    goal=f"Create a new repository on GitHub named {repo_name} with the provided description, create a branch '{branch_name}', manage the repository, create an issue titled '{issue_title}', add a file '{file_name}' with the provided content to the branch, and create a pull request '{pr_title}'.",
    backstory="The Scrum Master has excellent knowledge to ensure the creation and management of repositories on GitHub, facilitates the development team's workflow, and handles issue and branch management, including adding files to the repository and creating pull requests.",
    llm=my_llm,
    tools=[github_operations],
    verbose=True,
    allow_delegation=False,
)

scrum_master_task = Task(
    description=f"Create a new repository on GitHub named {repo_name} with the description '{description}', create a new branch '{branch_name}', create a new issue titled '{issue_title}' with description '{issue_body}', add a file '{file_name}' with the provided content to the branch, and create a pull request '{pr_title}' with description '{pr_body}'.",
    expected_output=f"A new repository on GitHub with the name '{repo_name}' and description '{description}', a new branch '{branch_name}' created, a new issue created with title '{issue_title}' and description '{issue_body}', a file '{file_name}' added to the branch with the provided content, and a pull request '{pr_title}' created with description '{pr_body}'.",
    agent=ScrumMaster,
    output_file="scrum_master_output.md",
)
