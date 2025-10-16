import requests
import streamlit as st

TOKEN = st.secrets["GITHUB_TOKEN"]
response = requests.get("https://api.github.com/user", headers={"Authorization": f"token {TOKEN}"})

if response.status_code == 200:
    st.success("Token is valid!")
    st.write(response.json())
else:
    st.error(f"Token failed: {response.status_code} - {response.text}")