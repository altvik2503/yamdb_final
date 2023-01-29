# FROM python:3.7-slim

# RUN apt update #

# RUN apt install -y gcc libpq-dev

# RUN mkdir /app

# COPY requirements.txt /app

# RUN pip3 install -r /app/requirements.txt --no-cache-dir

# COPY . /app

# WORKDIR /app

# CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
FROM python:3.7-slim

RUN apt update && apt install -y gcc libpq-dev

WORKDIR /app/api_yamdb

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
