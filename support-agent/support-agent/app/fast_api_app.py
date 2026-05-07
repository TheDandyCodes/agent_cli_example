# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging as python_logging

import google.auth
import telegram
from fastapi import FastAPI, Request
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import logging as google_cloud_logging

from app.app_utils.telemetry import setup_telemetry
from app.app_utils.typing import Feedback

setup_telemetry()
_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
python_logger.basicConfig(level=python_logging.INFO)

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")
telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
)
app.title = "support-agent"
app.description = "API for interacting with the Agent support-agent"


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram messages via webhook.

    Args:
        request: The incoming FastAPI request containing the Telegram Update.

    Returns:
        dict: Success status
    """
    if not telegram_token:
        python_logging.error("TELEGRAM_BOT_TOKEN not set")
        return {"status": "error", "message": "Bot token not configured"}

    bot = telegram.Bot(token=telegram_token)
    
    try:
        data = await request.json()
        update = telegram.Update.de_json(data, bot)
        
        if update.message and update.message.text:
            user_text = update.message.text
            chat_id = update.message.chat_id
            
            python_logging.info(f"Received message from {chat_id}: {user_text}")
            
            # Use the ADK app's runner to get a response from the agent
            # We use the chat_id as the session_id to maintain context per user
            response = await app.runner.run(
                user_text, 
                session_id=f"telegram_{chat_id}"
            )
            
            # Send the agent's response back to the user
            await bot.send_message(chat_id=chat_id, text=response.text)
            
        return {"status": "success"}
        
    except Exception as e:
        python_logging.error(f"Error processing Telegram webhook: {e}")
        return {"status": "error", "message": str(e)}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
