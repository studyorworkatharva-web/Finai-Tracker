from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserPublic
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user