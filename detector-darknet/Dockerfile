FROM debian:stretch

RUN apt-get update && apt-get install -y git build-essential
RUN mkdir -p /opt && cd /opt && git clone https://github.com/pjreddie/darknet.git \
   && cd darknet && make
RUN apt-get install -y curl
RUN cd /opt/darknet && curl -LO https://pjreddie.com/media/files/yolov3.weights
RUN apt-get install -y python-pip
RUN pip install bottle boto3

WORKDIR /app
ADD *.py /app

