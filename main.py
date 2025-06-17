from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional
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

@app.post("/user/webhook", response_model=WebhookResponse)
async def user_webhook(payload: WebhookRequest):
    logger.info(f"Received payload: {payload.json()}")
    return WebhookResponse(action="reply", data={"text": "Message received"})

