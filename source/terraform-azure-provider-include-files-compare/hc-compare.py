import requests
import os
import subprocess
from pprint import pprint
import re
import os

githubToken = os.getenv('GITHUB_TOKEN')
params = { "state": "open"}
headers = {'Authorization': f'token {githubToken}'}

metadataTag = "ms.custom:"
metadataTagSearchPattern = metadataTag + ".*"

urls =  [
            ["https://api.github.com/repos/MicrosoftDocs/azure-dev-docs-pr/contents/articles/terraform/includes/hashicorp-provider-versions-arm-2-70-0-to-current.md", 
             "https://api.github.com/repos/hashicorp/terraform-provider-azurerm/commits?path=CHANGELOG.md&sha=main"], 

            ["https://api.github.com/repos/MicrosoftDocs/azure-dev-docs-pr/contents/articles/terraform/includes/hashicorp-provider-versions-arm-2-0-0-to-2-69-0.md", 
             "https://api.github.com/repos/hashicorp/terraform-provider-azurerm/commits?path=CHANGELOG-v2.md&sha=main"]
        ]

# Clear the screen (works on Windows and Linux/macOS)
os.system('cls' if os.name == 'nt' else 'clear')

# For each docs/HashiCorp article(file) pair...
for urlPair in urls:

    # From the docs.microsoft.com version of the file, get the ms.custom metadata tag value that holds the commit SHA value of HashiCorp version of the file
    urlDocs = urlPair[0]
    response = requests.get(urlDocs, headers=headers, params=params)
    if (response.status_code == 200):
        fileinfo = response.json()
        if fileinfo['download_url']:
            f = requests.get(fileinfo['download_url'], headers=headers, params=params)

            filecontents = f.text

            commitIdDocsVersionOfArticle = re.search(metadataTagSearchPattern, filecontents)

            commitIdDocsVersionOfArticle = filecontents[commitIdDocsVersionOfArticle.start()+len(metadataTag):commitIdDocsVersionOfArticle.end()]
            commitIdDocsVersionOfArticle = commitIdDocsVersionOfArticle.strip()
            #print(f"docs: {commitIdDocsVersionOfArticle}")

    # From the HashiCorp repo, get the latest commit SHA value for the file
    urlHashiCorp = urlPair[1]
    response = requests.get(urlHashiCorp, headers=headers, params=params)
    if (response.status_code == 200):
        commitList = response.json()
        commitIdHashiCorp = commitList[0]['sha']
        #print(f"HashiCorp: {commitList[0]['sha']}")

    # If the two commit SHA values are different, send email to update the docs version
    if (commitIdDocsVersionOfArticle != commitIdHashiCorp):
        idx = urlDocs.rfind("/")
        fileNameDocs = urlDocs[idx+1:len(urlDocs)]
        print(f"{fileNameDocs} = OUT OF DATE.\nRetrieve from {urlHashiCorp}.")
    else:
        print(f"{fileNameDocs} = NO CHANGE.")
    print()