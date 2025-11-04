# ============================================================
# Auth Service - Dockerfile
# ============================================================

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Application Source ----
COPY . .

# ✅ Explicitly copy Alembic files (required for migrations)
COPY alembic.ini .
COPY alembic ./alembic

# Create a non-root user for security
RUN adduser --disabled-password appuser
USER appuser

# Expose the port
EXPOSE 8000

# ---- Command to run app ----
# Run Alembic manually when needed (not auto-run in production)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
