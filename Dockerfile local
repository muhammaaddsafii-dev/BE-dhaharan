# Menggunakan Python 3.11 dengan GDAL support untuk GeoDjango
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies untuk PostGIS/GeoDjango
RUN apt-get update && apt-get install -y \
    # PostgreSQL client
    postgresql-client \
    netcat \
    # GDAL/GEOS dependencies untuk GeoDjango - dengan versi spesifik
    gdal-bin \
    libgdal28 \
    libgdal-dev \
    libgeos-3.9.0 \
    libgeos-c1v5 \
    libgeos-dev \
    libproj-dev \
    # Build dependencies
    gcc \
    g++ \
    python3-dev \
    # Image processing
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set LD_LIBRARY_PATH to help find shared libraries
ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn untuk production
RUN pip install gunicorn

# Copy project files
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Copy entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]