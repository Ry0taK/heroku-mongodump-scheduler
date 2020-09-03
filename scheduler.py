#!/usr/bin/env python
import datetime
import subprocess
import requests
import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def send_discord(failed):

    discord_body = {
        "content": "MongoDB backup completed!"
    }

    if failed:
        discord_body = {
            "content": "MongoDB backup failed. Check console for more details."
        }

    requests.post(os.environ.get("DISCORD_WEBHOOK"), json.dumps(discord_body), headers={"Content-Type":"application/json"})

with open("credentials.json", mode="w") as f:
    f.write(os.environ.get("GOOGLE_CREDENTIALS_JSON"))

backup_name = "mongodump-{date}.gz".format(date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

process = subprocess.run(["mongodump", "--uri", os.environ.get("MONGODB_URI"), "--gzip", "--archive={backup_name}".format(backup_name=backup_name)])
if process.returncode != 0:
    send_discord(True)
    quit()

gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
drive = GoogleDrive(gauth)

results = drive.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))

#f = drive.CreateFile({"title": backup_name}) 
#f.SetContentFile(backup_name)
#f.Upload()

send_discord(False)
