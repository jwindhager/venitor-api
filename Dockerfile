FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

# upgrade to alpine3.9 for compatibility with Microsoft SQL driver
RUN sed s/3.8/3.9/ < /etc/apk/repositories > /etc/apk/repositories
RUN apk update
RUN apk upgrade --available && sync

# install Microsoft SQL driver
RUN apk add curl
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.5.2.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk

# install PyPI package dependencies
RUN apk add gcc g++ libffi-dev openssl-dev unixodbc-dev

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./app /app
