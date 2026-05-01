FROM python:3.12-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src/ src/
COPY frontend/ /usr/share/nginx/html

EXPOSE 80 8080

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8080 & nginx -g 'daemon off;'"]
