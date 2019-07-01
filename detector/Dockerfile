FROM debian:stretch

RUN apt-get update && apt-get install -y python-pip git
RUN pip install tensorflow
RUN pip install opencv-python
RUN apt-get install -y curl
RUN mkdir /app && cd /app && \
    git clone https://github.com/datitran/object_detector_app.git && \
    curl -LO http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017.tar.gz && \
    tar zxf faster_rcnn_resnet101_coco_11_06_2017.tar.gz && \
    rm -f faster_rcnn_resnet101_coco_11_06_2017.tar.gz && \
    cd faster_rcnn_resnet101_coco_11_06_2017 && \
    curl -LO https://raw.githubusercontent.com/tensorflow/models/477ed41e7e4e8a8443bc633846eb01e2182dc68a/object_detection/data/mscoco_label_map.pbtxt
RUN pip install pillow

WORKDIR /app
ADD *.py /app
