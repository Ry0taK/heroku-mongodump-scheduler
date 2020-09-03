#!/usr/bin/env python
import subprocess
import requests
import json
import os

process = subprocess.run(["mongodump", "--uri", os.environ.get("MONGODB_URI"), "--gzip", "--archive=backup.gz"])
if process.returncode != 0:
    send_discord(True)
    return

send_discord(False)
    

# TODO: Upload backup.gz to somewhere

def send_discord(failed):

    discord_body = {
        "content": "MongoDB backup completed!"
    }

    if failed:
        discord_body = {
            "content": "MongoDB backup failed. Check console for more details"
        }

    requests.post(os.environ.get("DISCORD_WEBHOOK"), json.dumps(discord_body), headers={"Content-Type":"application/json"})
