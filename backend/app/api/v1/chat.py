"""
Chat API - AI Chat Interface
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.ai.brain import AIBrain
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# This would be injected via dependency injection in production
ai_brain: Optional[AIBrain] = None


def set_ai_brain(brain: AIBrain):
    """Set AI Brain instance"""
    global ai_brain
    ai_brain = brain


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


@router.post("/message")
async def send_chat_message(chat_message: ChatMessage):
    """Send a chat message to AI"""
    if not ai_brain:
        raise HTTPException(status_code=503, detail="AI Brain is not available")
    
    try:
        response = await ai_brain.process_chat_message(
            message=chat_message.message,
            user_id=chat_message.user_id or "anonymous",
            context=chat_message.context or {}
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-script")
async def generate_script(
    intent: str = Body(...),
    parameters: Dict[str, Any] = Body(...)
):
    """Generate RouterOS script using AI"""
    if not ai_brain:
        raise HTTPException(status_code=503, detail="AI Brain is not available")
    
    try:
        script = await ai_brain.generate_routeros_script(intent, parameters)
        return {
            "script": script,
            "intent": intent,
            "parameters": parameters
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
