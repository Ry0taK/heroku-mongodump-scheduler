#!/usr/bin/env python
import subprocess
import requests
import json
import os

subprocess.run(["mongodump", "--uri", os.environ.get("MONGODB_URI"), "--gzip", "--archive=backup.gz"])

# TODO: Upload backup.gz to somewhere

discord_body = {
    "content": "MongoDB backup completed!"
}

requests.post(os.environ.get("DISCORD_WEBHOOK"), json.dumps(discord_body), headers={"Content-Type":"application/json"})
