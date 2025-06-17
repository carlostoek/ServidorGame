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

@app.post("/user/webhook")
async def user_webhook(payload: WebhookPayload):
    logging.info("Received webhook: %s", payload.json())

    # Placeholder logic - in the future implement bot logic here
    response = {"action": "reply", "data": {"text": "Message received"}}
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
