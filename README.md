# MAHInsight Backend (FastAPI)

This is a demo-ready backend for MAHInsight. It includes mock data generators, OpenAI integration stubs, and endpoints for sentiment, sales, heatmap and an executive chatbot.

Quickstart (local):

1. Create a virtualenv and install:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Set environment variables (create a .env):

OPENAI_API_KEY=your_key
DATABASE_URL=sqlite:///./mahinsight.db

3. Run:

```powershell
python main.py
```

Endpoints:
- /api/sentiment/*
- /api/sales/*
- /api/heatmap/*
- /api/chatbot/*

Notes:
- OpenAI integration requires a valid API key; for demo, functions will return parsed raw outputs.
- To connect real Twitter/YouTube APIs, update services/twitter_service.py and services/youtube_service.py.
