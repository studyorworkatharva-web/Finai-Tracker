from fastapi import APIRouter

router = APIRouter()

@router.get("/simulations")
def get_simulations():
    return {"message": "Financial simulation endpoint coming soon!"}
