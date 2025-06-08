FROM dockerhub.timeweb.cloud/python:3.10-slim

RUN apt-get update && apt-get install -y socat

RUN mkdir /app
WORKDIR /app

COPY . .

CMD socat TCP-LISTEN:2441,fork,reuseaddr EXEC:"python3 ./main.py"