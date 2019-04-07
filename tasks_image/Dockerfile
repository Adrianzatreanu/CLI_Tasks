FROM ubuntu:18.10

RUN apt-get update
RUN apt-get install -y python3.7 python3-pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python3.7 -m pip install --trusted-host pypi.python.org -r requirements.txt
COPY server.py /app/server.py

EXPOSE 80

CMD ["python3.7", "server.py"]
