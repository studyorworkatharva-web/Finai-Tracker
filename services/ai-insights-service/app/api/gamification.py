from fastapi import APIRouter

router = APIRouter()

@router.get("/gamification")
def get_gamification():
    return {"message": "Gamification and rewards endpoint coming soon!"}
