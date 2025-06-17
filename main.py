from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional, Callable
import logging

app = FastAPI(title="ServidorGame")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Metadata(BaseModel):
    timestamp: Optional[str] = None

class WebhookRequest(BaseModel):
    user_id: int
    message_type: str
    message_data: Any
    metadata: Optional[Metadata] = None

class WebhookResponse(BaseModel):
    action: str
    data: Optional[Dict[str, Any]] = None


def handle_start(payload: WebhookRequest) -> WebhookResponse:
    """Placeholder handler for /start command."""
    logger.info(f"Handling /start for user {payload.user_id}")
    return WebhookResponse(action="send_message", data={"text": "Welcome!"})


def handle_callback_query(payload: WebhookRequest) -> WebhookResponse:
    """Placeholder handler for callback queries."""
    logger.info(f"Handling callback query: {payload.message_data}")
    return WebhookResponse(action="answer_callback", data={"text": "Callback received"})


def handle_text_input(payload: WebhookRequest) -> WebhookResponse:
    """Placeholder handler for text inputs."""
    logger.info(f"Handling text input: {payload.message_data}")
    return WebhookResponse(action="reply", data={"text": "Text received"})


def handle_button_click(payload: WebhookRequest) -> WebhookResponse:
    """Placeholder handler for button clicks."""
    logger.info(f"Handling button click: {payload.message_data}")
    return WebhookResponse(action="reply", data={"text": "Button clicked"})


def handle_menu_selection(payload: WebhookRequest) -> WebhookResponse:
    """Placeholder handler for menu selections."""
    logger.info(f"Handling menu selection: {payload.message_data}")
    return WebhookResponse(action="reply", data={"text": "Menu option chosen"})

HANDLERS: Dict[str, Callable[[WebhookRequest], WebhookResponse]] = {
    "callback_query": handle_callback_query,
    "text": handle_text_input,
    "button_click": handle_button_click,
    "menu_selection": handle_menu_selection,
}


@app.post("/user/webhook", response_model=WebhookResponse)
async def user_webhook(payload: WebhookRequest):
    """Route incoming webhook payloads to the appropriate handler."""
    logger.info(f"Received payload: {payload.json()}")

    if payload.message_type == "command" and payload.message_data == "/start":
        return handle_start(payload)

    handler = HANDLERS.get(payload.message_type)
    if not handler:
        logger.error(f"Unhandled message type: {payload.message_type}")
        raise HTTPException(status_code=400, detail="Unknown message type")

    return handler(payload)

