import requests
import base64
import json
import datetime
from datetime import datetime
import os

# Clear the screen (works on Windows and Linux/macOS)
os.system('cls' if os.name == 'nt' else 'clear')

githubToken = os.getenv('GITHUB_TOKEN')

owner = input('What is the org name (owner) of the repo? ')
repo = input('What is the repo? ')
base_branch = 'main'
new_branch = 'test1'

# create new branch

def gh_sesh(user, token):
    s = requests.Session()
    s.auth = (user, token)
    s.headers = {'accept': 'application/vnd.github.v3+json'}
    return s

class GH_Response_Obj:
    def __init__(self, json_all, next_page):
        self.json_all = json_all
        self.next_page = next_page

def gh_get_request(gh_user, gh_token, url):
    headers = {'Authorization': "Token " + gh_token}
    response = requests.get(url, headers=headers)
    response_status = response.status_code
    
    if response_status > 200:
        print(f'\n This was the response code for the GET: {response_status}')
        exit()

    json = response.json()
    links = response.links

    try:
        next_page = links['next']['url']
    except:
        next_page = None

    full = GH_Response_Obj(json, next_page)

    return full

def gh_post_request(gh_user, gh_token, url, data):
    headers = {'Authorization': "Token " + gh_token}
    response1 = requests.get(url, headers=headers)
    r = response1.json()
    for br in r:
        if br['ref'] == f"refs/heads/{new_branch}" :
            print(f'already branch exist')
            return
    response = requests.post(url, data, headers=headers)
    response_status = response.status_code
    if response_status > 201:
        print(f'\n This was the response code for the POST: {response_status}')
        exit()

    json = response.json()

    return json 

def get_branch_sha(gh_user, gh_token, repo_name, branch_name="master"):
	url = f'https://api.github.com/repos/{owner}/{repo_name}/branches/{branch_name}'
	response =gh_get_request(gh_user, gh_token, url)
    
	sha = response.json_all['commit']['sha']
	return sha

def create_new_branch(gh_user, gh_token, master_branch_sha):
	now = str(datetime.now()).replace(' ', '__').replace(':', '-').replace('.', '')
	new_sync_branch = new_branch
	url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"

	data = {
		"ref": f'refs/heads/{new_sync_branch}',
		"sha": master_branch_sha
	}

	data = json.dumps(data)
    
	response =gh_post_request(gh_user, gh_token, url, data)
    
	return response

sha = get_branch_sha(owner, token, repo, base_branch)
new_sync_branch = create_new_branch(owner, token, sha)


# create a commit containing updated files

gitHubFileName = 'README.md'
fileName = 'README.md'

def push_to_repo_branch(gitHubFileName, fileName, repo_slug, branch, user, token):
    '''
    Push file update to GitHub repo
    
    :param gitHubFileName: the name of the file in the repo
    :param fileName: the name of the file on the local branch
    :param repo_slug: the github repo slug, i.e. username/repo
    :param branch: the name of the branch to push the file to
    :param user: github username
    :param token: github user token
    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    '''
    
    message = "Automated update " + str(datetime.now())
    path = "https://api.github.com/repos/%s/branches/%s" % (repo_slug, branch)
    r = requests.get(path, auth=(user,token))
    if not r.ok:
        print("Error when retrieving branch info from %s" % path)
        print("Reason: %s [%d]" % (r.text, r.status_code))
        raise
    rjson = r.json()
    treeurl = rjson['commit']['commit']['tree']['url']
    r2 = requests.get(treeurl, auth=(user,token))
    if not r2.ok:
        print("Error when retrieving commit tree from %s" % treeurl)
        print("Reason: %s [%d]" % (r2.text, r2.status_code))
        raise
    r2json = r2.json()
    sha = None

    for file in r2json['tree']:
        # Found file, get the sha code
        if file['path'] == gitHubFileName:
            sha = file['sha']

    # if sha is None after the for loop, we did not find the file name!
    if sha is None:
        print ("Could not find " + gitHubFileName + " in repos 'tree' ")
        raise Exception

    with open(fileName, 'rb') as data:
        content = base64.b64encode(data.read()).decode('utf-8')

    # gathered all the data, now let's push
    inputdata = {}
    inputdata["path"] = gitHubFileName
    inputdata["branch"] = branch
    inputdata["message"] = message
    inputdata["content"] = content
    if sha:
        inputdata["sha"] = str(sha)

    updateURL = "https://api.github.com/repos/" + repo_slug + "/contents/" + gitHubFileName
    try:
        rPut = requests.put(updateURL, auth=(user,token), data = json.dumps(inputdata))
        if not rPut.ok:
            print("Error when pushing to %s" % updateURL)
            print("Reason: %s [%d]" % (rPut.text, rPut.status_code))
            raise Exception
    except requests.exceptions.RequestException as e:
        print ('Something went wrong! I will print all the information that is available so you can figure out what happend!')
        print(rPut)
        print(rPut.headers)
        print(rPut.text)
        print(e)


# Create a PR from the commit

def create_pull_request(owner_name, repo_name, title, description, head_branch, base_branch, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        owner_name,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    response1 = requests.get(git_pulls_api, headers=headers)
    prs = response1.json()
    for pr in prs:
        if pr['head']['ref'] == head_branch:
            print("already exist PR")
            return
        else:
            r = requests.post(
                git_pulls_api,
                headers=headers,
                data=json.dumps(payload))
            if not r.ok:
                print("Request Failed: {0}".format(r.text))


push_to_repo_branch(gitHubFileName, fileName, f'{owner}/{repo}', new_branch, owner, githubToken)

create_pull_request(
    owner, # project_name
    repo, # repo_name
    "My pull request title", # title
    "My pull request description", # description
    new_branch, # head_branch
    base_branch, # base_branch
    githubToken, # git_token
)