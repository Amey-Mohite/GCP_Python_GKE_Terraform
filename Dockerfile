# Small, production-friendly base image
FROM python:3.12-slim

# --- Why these steps:
# 1) Keep image small and deterministic
# 2) Run as non-root for baseline security
# 3) Expose 8080 because we’ll use containerPort 8080 in Kubernetes
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies first for better layer caching
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app /app

# Create non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8080

# Run uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080"]
