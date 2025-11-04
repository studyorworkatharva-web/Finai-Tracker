# ============================================================
# Worker Service - Dockerfile
# ============================================================

# ---- Base Image ----
FROM python:3.11-slim

# ---- Environment Setup ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Working Directory ----
WORKDIR /app

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# ---- Copy Files ----
COPY requirements.txt .

# ---- Install Dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy App Source Code ----
COPY . .

# ---- Non-root User ----
RUN adduser --disabled-password workeruser
USER workeruser

# ---- Default command ----
# This assumes you have a main.py that runs a scheduler
CMD ["python", "main.py"]
