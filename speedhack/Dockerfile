FROM python:3.7-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "--factory", "speedhack.wsgi:application", "--host", "0.0.0.0", "--port", "8000"]
