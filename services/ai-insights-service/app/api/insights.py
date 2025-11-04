from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.gemini import get_gemini_response
from app.api.deps import get_current_user # Copied from Auth service
from app.db.models.user import User # Copied from Auth service

router = APIRouter()

class AIQueryRequest(BaseModel):
    user_prompt: str
    transactions_context: List[Dict[str, Any]] # e.g., [{"description": "Starbucks", "amount": 5.75}]

class AIQueryResponse(BaseModel):
    insight: str

@router.post("/query", response_model=AIQueryResponse)
def get_insights(
    request: AIQueryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generates AI insights based on a user's prompt and transaction context.
    """
    # 1. Create a structured prompt for the LLM
    transactions_str = "\n".join(
        [f"- {t.get('date')}: {t.get('description')} (${t.get('amount')})" for t in request.transactions_context]
    )
    
    prompt = f"""
    You are "FinAI", a calm, trustworthy, and modern financial assistant.
    You are speaking to {current_user.email}.
    
    Here is a list of their recent transactions:
    {transactions_str}
    
    The user asks: "{request.user_prompt}"
    
    Please provide a concise, helpful, and actionable response. 
    Use markdown for formatting if necessary (e.g., lists).
    """
    
    # 2. Get response from Gemini
    try:
        ai_response = get_gemini_response(prompt)
        return AIQueryResponse(insight=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... Other endpoints (Goal planning, simulation, etc.) ...