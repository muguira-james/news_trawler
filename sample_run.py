import feedparser
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue

from reuters_plugin import reuters_worker

# url = 'http://feeds.reuters.com/reuters/businessNews'
url = 'http://feeds.reuters.com/reuters/environment'
# d = feedparser.parse(url)
# for post in d.entries:
#   print(post.title)
"""
with urllib.request.urlopen(d.entries[0].link) as response:
   html_doc = response.read()

soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.get_text())

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# now get to the start of the story
#
art = soup.find(class_=re.compile("^ArticleBody_body")).get_text()

from gensim.summarization import summarize
ss = summarize(art, word_count=200)
"""
out_q = Queue()
reuters_worker(url, out_q)
