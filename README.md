# ServidorGame

This repository contains a simple FastAPI server used as the central controller for the *ClienteGame* Telegram bot. It exposes a single endpoint to handle incoming webhook events.

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
uvicorn app.main:app --reload
```

The server listens on `/user/webhook` for POST requests with JSON payloads describing Telegram bot messages.
