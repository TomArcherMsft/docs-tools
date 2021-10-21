import requests
import os
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

query_url = f"https://api.github.com/repos/{owner}/{repo}/{branch}/main"
commitSha = {}

r = requests.get(query_url, headers=headers, params=params)

branchinfo = r.json()

t = requests.get(branchinfo['commit']['commit']['tree']['url'], headers=headers, params=params)
treeinfo = t.json()

def loop(treeinfo):
 
    for treeitem in treeinfo:
        if treeitem['type'] == 'tree':
            i = requests.get(treeitem['url'], headers=headers, params=params)
            treeinfo_ = i.json()
            loop(treeinfo_['tree'])
        else:
            if treeitem['path'] == filename:
                f = requests.get(treeitem['url'], headers=headers, params=params)
                treeinfo_ = f.json()
                return treeinfo_

result = loop(treeinfo['tree'])

pprint(result)

pprint(r.json())