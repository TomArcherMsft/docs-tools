import requests
import os
import subprocess
from pprint import pprint

# Clear the screen (works on Windows and Linux/macOS)
os.system('cls' if os.name == 'nt' else 'clear')

githubToken = os.getenv('GITHUB_TOKEN')
params = { "state": "open"}
headers = {'Authorization': f'token {githubToken}'}

#owner = input('What is the org name (owner) of the repo? ')
#repo = input('What is the repo? ')
#branch = input('What is the branch? ')
#filename = input('What is the file name? ')
#query_url = f"https://api.github.com/repos/{owner}/{repo}/commits?path={filename}&sha={branch}"
query_url = "https://api.github.com/repos/hashicorp/terraform-provider-azurerm/commits?path=CHANGELOG.md&sha=main"

response = requests.get(query_url, headers=headers, params=params)
if (response.status_code == 200):
    commitList = response.json()
    print(f"sha: {commitList[0]['sha']}")
