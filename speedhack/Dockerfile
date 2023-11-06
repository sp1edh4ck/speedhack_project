FROM python:3.7-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip

# RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
