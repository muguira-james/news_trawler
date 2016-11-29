
import feedparser
from bs4 import BeautifulSoup
import requests
#import urllib2
import json
import datetime

import os,sys
from gensim.summarization import summarize
from gensim.summarization import keywords



### a class to tidy up the processing
class Article(object):
    def __init__(self, source, title, link, summ, keyw):
        # explicitly encode data as unicode
        self.source = source.encode('UTF-8', 'ignore')
        self.title = title.encode('UTF-8', 'replace')
        self.link = link.encode('UTF-8', 'ignore')
        self.summary = summ
        self.keywords = keyw


### this will dump the class variables as a dictionary
def jdefault(o):
    return o.__dict__
# -------------------------------------------------------------
def cnn_worker(url, output_q):
    d = feedparser.parse(url)
    for post in d.entries:
        # get the linked data...

        bb = requests.get(post.link)
        #
        # remove the html
        soup = BeautifulSoup(bb.text)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        # this is the body of cnn articles
        cc = soup.select('.zn-body-text')
        if len(cc) < 1:
            summ = 'pass'
            latentTopics = 'pass'
        else:
            text = cc[0].get_text()
            try:
                #
                # do my NLP work here
                #
                summ = summarize(text, word_count=100)

                latentTopics = "pass"
            except ValueError, TypeError:
                print('error: {}'.format(post.link))
            # keyw = keywords(text, ratio=0.01)
            # Article takes: source, title, and link
        ar = Article(url, post.title, post.link, summ, latentTopics)
        #
        ### dump it to json
        ar_json = json.loads(json.dumps(ar, default=jdefault))
        # save it in the output_q for later processing
        output_q.put(ar_json)
