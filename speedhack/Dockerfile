FROM python:3.7-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
