
import feedparser
from bs4 import BeautifulSoup
import urllib.request

import json
import datetime
import re

import os,sys
from gensim.summarization import summarize
from gensim.summarization import keywords

from multiprocessing import Process, Queue


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII") # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


### a class to tidy up the processing
class Article(object):
    def __init__(self, source, title, link, summ, keyw):
        # explicitly encode data as unicode
        self.source = source.encode('UTF-8', 'ignore')
        self.title = title.encode('UTF-8', 'replace')
        self.link = link.encode('UTF-8', 'ignore')
        self.summary = summ
        self.keywords = keyw

# -------------------------------------------------------------
def getArticleKeywordsSummary(posting):
    with urllib.request.urlopen(posting.link) as response:
       html_doc = response.read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.get_text())

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # now get to the start of the story
    #
    art = soup.find(class_=re.compile("^ArticleBody_body")).get_text()

    summ = summarize(art, word_count=200)
    keyw = keywords(art)
    return summ,keyw
# -------------------------------------------------------------
def reuters_worker(url, output_q):
    d = feedparser.parse(url)
    for post in d.entries:
        print(post.title)
        #
        # I would do my NLP work here
        #
        summ,keyw = getArticleKeywordsSummary(post)
        #
        # Article takes: source, title, and link
        ar = Article(url, post.title, post.link, summ, keyw)
        # debugging and testing
        sss = ar.__dict__
        ar_json = json.dumps(sss, cls=MyEncoder)
        # print(ar_json)
        #
        ### dump it to json
        #
        output_q.put(ar_json)
