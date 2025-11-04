# app/api/insights.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.gemini import get_gemini_response
from app.api.deps import get_current_user  # Handles JWT extraction

router = APIRouter()

class AIQueryRequest(BaseModel):
    user_prompt: str
    transactions_context: List[Dict[str, Any]]  # [{"description": "Starbucks", "amount": 5.75}]

class AIQueryResponse(BaseModel):
    insight: str

@router.post("/query", response_model=AIQueryResponse)
def get_insights(
    request: AIQueryRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generates AI insights based on a user's prompt and transaction context.
    """
    user_email = current_user.get("email", "the user")
    user_id = current_user.get("user_id", "unknown")

    # 1. Create structured prompt for Gemini
    transactions_str = "\n".join(
        [f"- {t.get('date', '')}: {t.get('description', '')} (${t.get('amount', '')})"
         for t in request.transactions_context]
    )

    prompt = f"""
    You are "FinAI", a calm, trustworthy, and modern financial assistant.
    You are speaking to {user_email} (user ID: {user_id}).

    Here is a list of their recent transactions:
    {transactions_str}

    The user asks: "{request.user_prompt}"

    Please provide a concise, helpful, and actionable response. 
    Use markdown for formatting if necessary (e.g., lists).
    """

    # 2. Get AI response
    try:
        ai_response = get_gemini_response(prompt)
        return AIQueryResponse(insight=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")
