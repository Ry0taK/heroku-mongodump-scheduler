#!/usr/bin/env python
import subprocess
import requests
import json
import os

print(subprocess.run(["mongodump", "--uri", os.environ.get("MONGODB_URI"), "--gzip", "--archive=backup.gz"], capture_output=True))

discord_body = {
    "content": "MongoDB backup completed!"
}

requests.post(os.environ.get("DISCORD_WEBHOOK"), json.dumps(discord_body), headers={"Content-Type":"application/json"})
