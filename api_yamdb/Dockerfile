FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y gcc libpq-dev

WORKDIR /app/api_yamdb

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
