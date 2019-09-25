#!/usr/bin/env python

from bottle import route, run, template, request, post
import queue
import images
import sql
import os
import json
import time


db = sql.Db(os.getenv("db_host"), os.getenv("db_name"),
            os.getenv("db_user"), os.getenv("db_pass"))
db.create_tables()

send_queue = os.getenv("send_queue")
q = queue.Queue(send_queue)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        

def enqueue(num):
    sent = 0
    for url in images.get_images(num):
        msg = json.dumps({ "url": url })
        q.send(msg)
        sent += 1
    return sent


@route('/')
def index():
    # queue new
    num_queued = 0
    if request.params.get("enqueue"):
        num_queued = enqueue(int(request.params.get("enqueue")))

    # render page
    args = {
        "num_queued": num_queued,
        "queue_depth": q.depth(),
        "obj_counts": db.get_object_counts()
    }
    return template("templates/index.html", **args)


@route('/images')
def images_page():
    obj = request.params.get("obj")
    start_date = request.params.get("date") or 0
    next_date = 0
    cols = request.params.get("cols") or 3
    rows = request.params.get("rows") or 20
    if not obj:
        return index()

    limit = rows*cols
    urls = db.get_urls_by_obj(obj, int(start_date), limit+1)
    if len(urls) > limit:
        next_date = urls[-1]["inserted_at"]
        urls = urls[0:limit]
        
    # render page
    args = {
        "obj": obj,
        "rows": chunks(urls, cols),
        "next_date": next_date,
    }
    return template("templates/images.html", **args)


@post('/detect_reply')
def detect_reply():
    # stores image in db with objects detected
    msg = json.load(request.body)
    for o in msg["objects"]:
        db.insert_url(msg["url"], o, int(time.time() * 1000))
    return "OK"

run(host='0.0.0.0', port=8080)

