from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ServidorGame")

class WebhookPayload(BaseModel):
    user_id: int
    message_type: str
    message_data: Optional[str] = None
    timestamp: Optional[float] = Field(default_factory=lambda: datetime.utcnow().timestamp())
    metadata: Optional[Dict] = None


async def handle_start(payload: WebhookPayload):
    """Handle the /start command."""
    logging.info("Handling /start for user %s", payload.user_id)
    return {"action": "reply", "data": {"text": "Welcome to ServidorGame!"}}


async def handle_callback_query(payload: WebhookPayload):
    """Handle callback queries triggered by inline buttons."""
    logging.info(
        "Handling callback query for user %s: %s", payload.user_id, payload.message_data
    )
    return {"action": "reply", "data": {"text": "Callback processed"}}


async def handle_text_input(payload: WebhookPayload):
    """Handle regular text messages."""
    logging.info(
        "Handling text input for user %s: %s", payload.user_id, payload.message_data
    )
    return {"action": "reply", "data": {"text": "Text received"}}


async def handle_button_click(payload: WebhookPayload):
    """Handle generic button clicks."""
    logging.info(
        "Handling button click for user %s: %s", payload.user_id, payload.message_data
    )
    return {"action": "reply", "data": {"text": "Button clicked"}}


async def handle_menu_selection(payload: WebhookPayload):
    """Handle menu selections from custom keyboards or menus."""
    logging.info(
        "Handling menu selection for user %s: %s", payload.user_id, payload.message_data
    )
    return {"action": "reply", "data": {"text": "Menu option chosen"}}

@app.post("/user/webhook")
async def user_webhook(payload: WebhookPayload):
    """Route incoming messages to the appropriate handler."""
    logging.info("Received webhook: %s", payload.json())

    if payload.message_type == "text":
        if payload.message_data and payload.message_data.startswith("/start"):
            return await handle_start(payload)
        return await handle_text_input(payload)

    if payload.message_type == "callback_query":
        return await handle_callback_query(payload)

    if payload.message_type == "button_click":
        return await handle_button_click(payload)

    if payload.message_type == "menu_selection":
        return await handle_menu_selection(payload)

    logging.warning("Unknown message type: %s", payload.message_type)
    raise HTTPException(status_code=400, detail="Unknown message type")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
