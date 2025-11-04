from fastapi import APIRouter

router = APIRouter()

@router.get("/goals")
def get_goals():
    return {"message": "Goal management endpoint coming soon!"}
