FROM python:3.12-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "speedhack.wsgi:application", "--bind", "0:8000"]