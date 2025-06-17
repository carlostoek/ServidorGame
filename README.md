# ServidorGame

FastAPI server for handling messages from the Telegram bot ClienteGame.

The `/user/webhook` endpoint now routes incoming messages to internal
placeholder handlers based on the `message_type` field. Supported types are:

* `/start` command
* `callback_query`
* `text`
* `button_click`
* `menu_selection`

## Running

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
