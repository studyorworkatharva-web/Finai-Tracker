# ============================================================
# Transactions Service - Dockerfile
# ============================================================

# Base image
FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# ✅ Explicitly copy Alembic files
COPY alembic.ini .
COPY alembic ./alembic

# ✅ Ensure ML model exists (warn if missing but don’t fail build)
RUN test -f ml/model.joblib || echo "⚠️  Warning: ml/model.joblib not found. Train or add it before deployment."

# ✅ Security: run as non-root user
RUN adduser --disabled-password appuser
USER appuser

# Expose app port
EXPOSE 8000

# ✅ Run Alembic + Start App
# (Optional: uncomment next line if you want auto-migrations on container start)
# CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

# Default CMD (manual Alembic)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
