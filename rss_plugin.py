
import feedparser
from bs4 import BeautifulSoup
import urllib.request

import json
import datetime
import re

import os,sys

#
# a simple, but not fool proof way to create json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII") # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


### a class to tidy up the processing
class Article(object):
    def __init__(self, source, title, link, summ, keyw):
        # explicitly encode data as ASCII
        self.source = source.encode('UTF-8', 'ignore')
        self.title = title.encode('UTF-8', 'replace')
        self.link = link.encode('UTF-8', 'ignore')
        self.summary = summ
        self.keywords = keyw

# -------------------------------------------------------------
#
# loop - gather all rss data from the URL
def rss_worker(url, output_q):
    d = feedparser.parse(url)
    for post in d.entries:
        print(post.title)
        #
        # I would do my NLP work here
        #
        summ = "pass"
        keyw = "pass"
        #
        # Article takes: source, title, and link
        ar = Article(url, post.title, post.link, summ, keyw)
        # debugging and testing
        sss = ar.__dict__
        ar_json = json.dumps(sss, cls=MyEncoder)
        # print(ar_json)
        #
        ### dump it to json and send back to main loop for storage
        #
        output_q.put(ar_json)
