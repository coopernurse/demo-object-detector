FROM debian:stretch

RUN apt-get update && apt-get install -y python-pip python-mysqldb
RUN pip install bottle boto3
RUN pip install requests
RUN mkdir -p /app
WORKDIR /app
ADD *.py /app/
ADD templates/ /app/templates/