#!/usr/bin/env python

import re
import requests

def images_from_html(html):
    # skip to "imgcontainer" div
    pos = html.find("imgcontainer")
    if pos > 0:
        html = html[pos:]
    img_regex = r"<img .+ src=['\"](.+)['\"]"        
    matches = re.finditer(img_regex, html, re.MULTILINE)
    return [ m.group(1) for m in matches ]


def links_from_html(html):
    # skip to "imgcontainer" div
    pos = html.find("imgcontainer")
    if pos > 0:
        html = html[pos:]
    img_regex = r"<a href=['\"](.+)['\"]"        
    matches = re.finditer(img_regex, html, re.MULTILINE)
    return set([ m.group(1) for m in matches if "free-photos" in m.group(1) ])


def download_url_from_html(html):
    # skip to "imgcontainer" div
    pos = html.find("detail_content")
    if pos > 0:
        html = html[pos:]
    img_regex = r"<a .+ href=['\"]([^'\"]+)['\"]"
    matches = re.finditer(img_regex, html, re.MULTILINE)
    urls = [ m.group(1) for m in matches ]
    return urls[0] if len(urls) > 0 else None


def get_page_body(s, u):
    resp = s.get(u)
    return resp.text

def get_image_urls():
    # returns 50 different random jpeg urls
    s = requests.Session()
    free_pic_url = "http://absfreepic.com/free-photos/free_photos.html"
    contents = get_page_body(s, free_pic_url)
    urls = []
    for u in links_from_html(contents):
        resp = get_page_body(s, u)
        dl_url = download_url_from_html(resp)
        if dl_url:
            urls.append(dl_url)
    return urls
        

def get_images(num):
    gen = 0
    i = 0
    urls = []
    while gen < num:
        if i >= len(urls):
            urls = get_image_urls()
            i = 0
        yield urls[i]
        i += 1
        gen += 1

if __name__ == "__main__":
    for i in get_image_urls():
        print i
