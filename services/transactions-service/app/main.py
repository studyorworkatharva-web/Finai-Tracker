from fastapi import FastAPI
from app.api import transactions  # make sure this folder and router exist

app = FastAPI(title="Transactions Service")

# Include routes
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "transactions"}
