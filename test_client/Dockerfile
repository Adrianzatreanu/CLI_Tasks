FROM python:3.7.1-stretch

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY client.py /app/client.py
