import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Gemini: {e}")

# Configure safety settings for generative model
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the text response.
    """
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set. Returning mock response.")
        return "This is a mock AI response. Please set your GEMINI_API_KEY."

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # Use a fast, modern model
            safety_settings=safety_settings
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        raise HTTPException(status_code=500, detail=f"Error communicating with AI service: {e}")