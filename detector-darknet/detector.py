#!/usr/bin/env python

from bottle import route, run, template, request, post
from subprocess import Popen, PIPE
import re
import os
import boto3
import json
import urllib2


sqs = boto3.resource("sqs")
reply_queue = sqs.create_queue(QueueName=os.getenv("reply_queue"))


def parse_output(output, thresh=90):
    objs = set()
    regex = r"(\w+): (\d+)%"    
    for line in output.split("\n"):
        line = line.strip()
        matches = re.finditer(regex, line, re.MULTILINE)
        for m in matches:
            obj = m.group(1)
            pct = int(m.group(2))
            if pct >= thresh:
                objs.add(obj)
    print "OUTPUT: %s" % output
    print "  OBJS: %s" % objs
    return { "objects": list(objs) }


def classify_file(fname):
    process = Popen(["/opt/darknet/darknet", "detect", "/opt/darknet/cfg/yolov3.cfg",
                     "/opt/darknet/yolov3.weights", fname], stdout=PIPE, cwd="/opt/darknet")
    (output, err) = process.communicate()
    exit_code = process.wait()
    return parse_output(output)

    
@route('/')
def home():
  return "OK"

@post('/detect_request')
def detect_request():
  # stores image in db with objects detected
  outfile = "/tmp/img.jpg"
  msg = json.load(request.body)
  response = urllib2.urlopen(msg["url"])
  out = open(outfile, "wb")    
  out.write(response.read())
  out.close()
  detect_out = classify_file(outfile)
  os.remove(outfile)
  # send reply to return queue
  outmsg = json.dumps({"url": msg["url"], "objects": detect_out["objects"]})
  print "done: %s" % outmsg
  reply_queue.send_message(MessageBody=outmsg)
  return "OK"

print "starting web server"
run(host='0.0.0.0', port=8080)
