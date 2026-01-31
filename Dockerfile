# Production Dockerfile for Google Cloud Run
FROM python:3.11-slim-bullseye

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal28 \
    libgdal-dev \
    libgeos-3.9.0 \
    libgeos-c1v5 \
    libgeos-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set library paths
ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Collect static files (ignore errors if no static files yet)
RUN python manage.py collectstatic --noinput || true

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start Gunicorn
# Use exec to ensure proper signal handling
# Bind to PORT environment variable (Cloud Run injects this)
CMD exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 2 \
    --threads 4 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --log-level info