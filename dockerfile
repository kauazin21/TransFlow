FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/app/src"

# permite que o docker-compose sobrescreva o comando
ENTRYPOINT []
CMD ["python", "src/main.py"]
