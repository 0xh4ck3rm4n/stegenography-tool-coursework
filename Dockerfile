# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set metadata labels for GHCR
LABEL org.opencontainers.image.source="https://github.com/0xh4ck3rm4n/steganography-tool-coursework"
LABEL org.opencontainers.image.description="Steganography Tool - Hide messages in images"
LABEL org.opencontainers.image.licenses="MIT"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DISPLAY=:0

# Install system dependencies for Pillow and Tkinter
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    tcl \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxinerama1 \
    libxi6 \
    libxrandr2 \
    libxcursor1 \
    libxtst6 \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY LICENSE ./
COPY README.md ./

# Create images directory for user data
RUN mkdir -p /app/images

# Set permissions
RUN chmod -R 755 /app

# Expose display for GUI (optional, for documentation)
# Users will need to mount X11 socket or use VNC

# Default command to run the application
CMD ["python", "main.py"]

