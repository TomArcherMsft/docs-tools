import requests
import os
import subprocess
from pprint import pprint

# Clear the screen (works on Windows and Linux/macOS)
os.system('cls' if os.name == 'nt' else 'clear')

githubToken = os.getenv('GITHUB_TOKEN')
print(githubToken)

params = { "state": "open"}
headers = {'Authorization': f'token {githubToken}'}

#owner = input('What is the org name (owner) of the repo? ')
#repo = input('What is the repo? ')
#branch = input('What is the branch? ')
#filename = input('What is the file name? ')
#query_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filename}"
#query_url = "https://api.github.com/repos/MicrosoftDocs/azure-dev-docs-pr/contents/articles/terraform/includes/hashicorp-provider-versions-arm-2-70-0-to-current.md"
query_url = "https://api.github.com/repos/MicrosoftDocs/azure-dev-docs/contents/articles/terraform/includes/hashicorp-provider-versions-arm-2-70-0-to-current.md"

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