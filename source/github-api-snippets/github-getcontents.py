import requests
import os
import subprocess
from pprint import pprint

# Clear the screen (works on Windows and Linux/macOS)
os.system('cls' if os.name == 'nt' else 'clear')

githubToken = os.getenv('GITHUB_TOKEN')

params = { "state": "open"}
headers = {'Authorization': f'token {githubToken}'}

owner = input('What is the org name (owner) of the repo? ')
repo = input('What is the repo? ')
branch = input('What is the branch? ')
filename = input('What is the file name? ')
query_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filename}"

response = requests.get(query_url, headers=headers, params=params)
if (response.status_code == 200):
    fileinfo = response.json()
    if fileinfo['download_url']:
        f = requests.get(fileinfo['download_url'], headers=headers, params=params)
        filecontents = f.text
        print('\n---------------------------------- file contents ----------------------------------')
        pprint(filecontents)
else:
    print(f"GET {query_url}\nStatus code = {response.status_code}\n")