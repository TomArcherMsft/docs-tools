import requests
import os
import subprocess
from pprint import pprint

githubToken = os.getenv('GITHUB_TOKEN')
params = { "state": "open"}
headers = {'Authorization': f'token {githubToken}'}

os.system('cls' if os.name == 'nt' else 'clear')

owner = input('What is the org name (owner) of the repo? ')
repo = input('What is the repo? ')
branch = input('What is the branch? ')
filename = input('What is the file name? ')
query_url = f"https://api.github.com/repos/{owner}/{repo}/commits?path={filename}&sha={branch}"

response = requests.get(query_url, headers=headers, params=params)
if (response.status_code == 200):
    commitList = response.json()
    print(f"sha: {commitList[0]['sha']}")
