FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5002", "maze_escape:app", "-w", "1", "--threads", "8", "--worker-class", "gthread"]
