from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.db.session import engine, Base

# Create all tables (Alembic is preferred for production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinAI Auth Service",
    description="Handles user authentication, registration, and profile management.",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Local frontend
    "https://your-vercel-frontend.vercel.app",  # Deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", summary="Health Check", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)