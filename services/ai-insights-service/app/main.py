from fastapi import FastAPI
from app.api import insights, goals, simulations, gamification  # optional, modularize later

app = FastAPI(title="AI Insights Service")

# Include your route modules
app.include_router(insights.router, prefix="/ai", tags=["AI Insights"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])
app.include_router(simulations.router, prefix="/simulate", tags=["Simulations"])
app.include_router(gamification.router, prefix="/gamify", tags=["Gamification"])

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ai-insights"}
