FROM python:3.7-slim

WORKDIR /app

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "speedhack.wsgi:application", "--bind", "0:8000"]