FROM selenium/standalone-chrome:114.0

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "/app/bot.py"]
