
import feedparser
import urllib2
import json


### a class to tidy up the processing
class Article(object):
    def __init__(self, source, title, link):
        # explicitly encode data as unicode
        self.source = source.encode('UTF-8', 'ignore')
        self.title = title.encode('UTF-8', 'replace')
        self.link = link.encode('UTF-8', 'ignore')


### this will dump the class variables as a dictionary
def jdefault(o):
    return o.__dict__
# -------------------------------------------------------------
def rss_worker(url, output_q):
    d = feedparser.parse(url)
    for post in d.entries:
        # Article takes: source, title, and link
        ar = Article(url, post.title, post.link)
        #
        # do my NLP work here
        #
        ### dump it to json
        ar_json = json.loads(json.dumps(ar, default=jdefault))
        # save it in the output_q for later processing
        output_q.put(ar_json)
