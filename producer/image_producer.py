#!/usr/bin/env python

import urllib2
import re


def images_from_html(html):
    # skip to "imgcontainer" div
    pos = html.find("imgcontainer")
    if pos > 0:
        html = html[pos:]
    img_regex = r"<img .+ src=['\"](.+)['\"]"        
    matches = re.finditer(img_regex, html, re.MULTILINE)
    return [ m.group(1) for m in matches ]


def get_image_urls():
    # returns 50 different random jpeg urls
    free_pic_url = "http://absfreepic.com/free-photos/free_photos.html"
    resp = urllib2.urlopen(free_pic_url)
    contents = resp.read()
    resp.close()


f = open("/tmp/foo.html")
images = images_from_html(f.read())
f.close()

for i in images:
    print i
