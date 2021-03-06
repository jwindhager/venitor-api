FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

RUN apk update
RUN apk add gcc g++ unixodbc unixodbc-dev
RUN apk add libffi libffi-dev openssl openssl-dev

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./app /app
