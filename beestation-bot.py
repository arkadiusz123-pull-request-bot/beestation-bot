# this script was made by
# gang weed
import requests
import simplejson as json
import codecs
import subprocess
from requests.auth import HTTPBasicAuth

# Vars, this is the bot's config
username = '' # your/the bot's username/email
password = '' # your/the bot's password
upstream = 'https://api.github.com/repos/' # the repo you're mirroring FROM. ex: "https://api.github.com/repos/tgstation/tgstation/pulls"
downstream = 'https://api.github.com/repos/' # The repo you're mirroring TO. ex: 'https://api.github.com/repos/beestation/beestation/pulls'

# get list of already seen PRs from text file
oldprs = open("oldprs.txt").readlines()
oldfinal = []
for old in oldprs:
    oldfinal.append(old.replace('\n', ''))
writeprs = []


# get prs from /tg/
f = requests.get(upstream+"/pulls?per_page=100", auth=HTTPBasicAuth(username, password))
try:
    f.raise_for_status()
except:
    print("[Cant raise request]")
try:
    obj = json.loads(f.content.decode('utf-8'))
except:
    print("[Cant load request]")

# parse /tg/ PRs
for x in obj:
    if str(x['id']) in oldfinal:
        writeprs.append(str(x['id']))
    else:
        base = x["head"]
        postd = {
        "title": "[PR MIRROR]: " + str(x["title"]),
        "body": "Original Author: "+str(x["user"]["login"])+"\n"+"Original Pull Request: "+str(x["html_url"])+"\n\n"+str(x["body"]),
        "head": base["label"],
        "base": "master",
        "maintainer_can_modify": False
        }
        r = requests.post(downstream+'/pulls', auth=HTTPBasicAuth(username, password), json=postd)
        try:
            r.raise_for_status()
        except:
            print("[Not Raisable]")
        try:
            robj = json.loads(r.content.decode('utf-8'))
            print(robj)
        except:
            print("[Not Extractable]")
        print("")
        writeprs.append(str(x['id']))

with open('oldprs.txt', mode='wt', encoding='utf-8') as myfile:
    for lines in writeprs:
        myfile.write(str(lines)+'\n')
