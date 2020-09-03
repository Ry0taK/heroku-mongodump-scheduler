#!/usr/bin/env python
import datetime
import subprocess
import requests
import json
import os

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

process = subprocess.run(["mongodump", "--uri", os.environ.get("MONGODB_URI"), "--gzip", "--archive=mongodump-{date}.gz".format(date=datetime.datetime.now().strftime('%Y%m%d%H%M%S'))])
if process.returncode != 0:
    send_discord(True)
    quit()

# TODO: Upload backup.gz to Google Drive

send_discord(False)
