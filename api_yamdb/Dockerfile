FROM python:3.7-slim

RUN apt update && apt install -y gcc libpq-dev

COPY api_yamdb/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./api_yamdb /app

WORKDIR /app/api_yamdb

CMD ["gunicorn", "/app/api_yamdb.wsgi:application", "--bind", "0:8000" ]
