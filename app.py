import requests
import base64
from datetime import date, datetime
import streamlit as st

# Constants
REPO = "lindaclaassen89-oss/TestDateLogging"
FILE_PATH = "date_log.txt"
BRANCH = "main"
TOKEN = st.secrets["GITHUB_TOKEN"]
TODAY = str(datetime.now())

# GitHub API URL
url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

# Get the current file SHA (needed for updates)
response = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
if response.status_code == 200:
    content = response.json()
    sha = content["sha"]
    existing_content = base64.b64decode(content["content"]).decode()
else:
    sha = None
    existing_content = ""

# Append today's date if not already logged
if TODAY not in existing_content:
    new_content = existing_content + f"{TODAY}\n"
    encoded_content = base64.b64encode(new_content.encode()).decode()

    data = {
        "message": f"Log run on {TODAY}",
        "content": encoded_content,
        "branch": BRANCH,
        "sha": sha
    }

    update_response = requests.put(url, json=data, headers={"Authorization": f"token {TOKEN}"})
    if update_response.status_code == 200 or update_response.status_code == 201:
        st.success("Date logged successfully to GitHub!")
    else:
        st.error(f"Failed to update file: {update_response.json()}")
else:
    st.info("Date already logged.")