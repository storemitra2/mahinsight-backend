import streamlit as st
import requests
from typing import Any, Dict

API_BASE = st.secrets.get('API_BASE', 'http://localhost:8000')

@st.cache_data
def call_api(path: str, method: str = 'GET', json: Dict = None, files: Dict = None) -> Any:
    url = f"{API_BASE}{path}"
    try:
        if method=='GET':
            r = requests.get(url, timeout=30)
        else:
            r = requests.post(url, json=json, files=files, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def analyze_text(text: str):
    return call_api('/api/sentiment/analyze', method='POST', json={'text': text})
