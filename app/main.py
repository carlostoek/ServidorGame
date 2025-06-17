from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import logging
from datetime import datetime
import os
import httpx

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ServidorGame")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_VIP_CHANNEL_ID = os.getenv("TELEGRAM_VIP_CHANNEL_ID")
TELEGRAM_ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID")

class WebhookPayload(BaseModel):
    user_id: int
    message_type: str
    message_data: Optional[str] = None
    timestamp: Optional[float] = Field(default_factory=lambda: datetime.utcnow().timestamp())
    metadata: Optional[Dict] = None


async def is_user_vip(user_id: int) -> bool:
    """Check if the user is part of the VIP channel."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_VIP_CHANNEL_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
    params = {"chat_id": TELEGRAM_VIP_CHANNEL_ID, "user_id": user_id}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok") and data.get("result"):
                    status = data["result"].get("status")
                    if status in {"member", "administrator", "creator"}:
                        return True
    except Exception as exc:  # pragma: no cover - network errors ignored in tests
        logging.warning("VIP check failed: %s", exc)

    return False


async def get_user_role(user_id: int) -> str:
    """Return the role for the given user id."""
    if TELEGRAM_ADMIN_ID and str(user_id) == TELEGRAM_ADMIN_ID:
        return "admin"
    if await is_user_vip(user_id):
        return "vip"
    return "free"


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

    user_role = await get_user_role(payload.user_id)

    response = None

    if payload.message_type == "text":
        if payload.message_data and payload.message_data.startswith("/start"):
            response = await handle_start(payload)
        else:
            response = await handle_text_input(payload)

    elif payload.message_type == "callback_query":
        response = await handle_callback_query(payload)

    elif payload.message_type == "button_click":
        response = await handle_button_click(payload)

    elif payload.message_type == "menu_selection":
        response = await handle_menu_selection(payload)
    else:
        logging.warning("Unknown message type: %s", payload.message_type)
        raise HTTPException(status_code=400, detail="Unknown message type")

    if isinstance(response, dict):
        response["user_role"] = user_role
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
