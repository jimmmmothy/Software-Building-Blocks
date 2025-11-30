# Use a lightweight Python base image (no CUDA/GPU)
FROM python:3.12-slim

WORKDIR /app

COPY dependencies/docker.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        wget \
        cmake \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        torch==2.9.1+cpu --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r docker.txt

COPY controller.py .
COPY services/ ./services/

EXPOSE 5000

CMD ["python", "controller.py"]
