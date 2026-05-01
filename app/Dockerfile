# ─── Stage 1: Build ───────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy only requirements first (layer caching optimization)
COPY requirements.txt .

# Install dependencies into a local folder (not system)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="devops-fresher"
LABEL description="DevOps 101 Task Manager - A beginner DevOps learning project"

# Security: create a non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY app.py .

# Set environment variables with safe defaults
ENV FLASK_DEBUG=false \
    APP_VERSION=1.0.0 \
    ENV_NAME=production \
    PORT=5000

# Expose the application port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Health check baked into the image
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Start with gunicorn (production-grade WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
