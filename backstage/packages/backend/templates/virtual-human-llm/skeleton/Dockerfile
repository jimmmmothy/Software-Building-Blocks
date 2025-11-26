FROM nvcr.io/nvidia/pytorch:24.05-py3

WORKDIR /app

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

COPY dependencies/docker.txt .
RUN pip install --no-cache-dir -r docker.txt

COPY controller.py .
COPY Service/ ./Service/

EXPOSE 5000

CMD ["python", "controller.py"]
