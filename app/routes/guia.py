from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.controllers.guia_controller import get_chat_response

router = APIRouter()

@router.post("/chat", response_model=Dict[str, str])
async def chat_route(messages: List[Dict[str, str]], model: str = "lmstudio-community/Phi-3.1-mini-4k-instruct-GGUF", temperature: float = 0.7):
    response = await get_chat_response(messages, model, temperature)
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    return response
