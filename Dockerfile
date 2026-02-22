FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/0xh4ck3rm4n/steganography-tool-coursework"
LABEL org.opencontainers.image.description="Steganography Tool - Hide messages in images"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DISPLAY=:0

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

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY LICENSE ./
COPY README.md ./

RUN mkdir -p /app/images

RUN chmod -R 755 /app

ENTRYPOINT ["python", "main.py"]
CMD ["--cli"]