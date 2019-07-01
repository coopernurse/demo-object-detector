#!/usr/bin/python

# based on: 
# https://github.com/tensorflow/models/blob/477ed41e7e4e8a8443bc633846eb01e2182dc68a/object_detection/object_detection_tutorial.ipynb

import os
import os.path
import sys
sys.path.insert(0, '/app/object_detector_app')

import numpy as np
import tensorflow as tf
from PIL import Image
from object_detection.utils import label_map_util
import json

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

infile = sys.argv[1]
min_score = .7

PATH_TO_CKPT = "faster_rcnn_resnet101_coco_11_06_2017/frozen_inference_graph.pb"
PATH_TO_LABELS = "faster_rcnn_resnet101_coco_11_06_2017/mscoco_label_map.pbtxt"
NUM_CLASSES = 90
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def classify_file(infile):
    image = Image.open(infile)
    image_np = load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    sess = tf.Session(graph=detection_graph)

    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    objects = {}
    for i in range(0, len(classes[0])):
        name = category_index.get(classes[0][i], {}).get("name", None)
        if name:
            if scores[0][i] >= min_score and name not in objects:
                objects[name] = float(scores[0][i])
    return {
        "file": infile,
        "objects": objects
    }


if os.path.isdir(infile):
    for (dirpath, dirnames, filenames) in os.walk(infile):
        for f in filenames:
            print json.dumps(classify_file(os.path.join(dirpath, f)))
        break
else:
    print json.dumps(classify_file(infile))

