
# -*- coding: utf-8 -*-
import time
import os
from pymongo import MongoClient
from multiprocessing import Process, Queue
import logging
import json
from rss_plugin import rss_worker
# ----------------------------------------------------------

logging.basicConfig(filename='log.log',
                    format='%(asctime)s %(message)s:',
                    level=logging.DEBUG)

logging.info('Trawler startup:')
logging.info('Step 0: fetch configuration structure')

config = json.loads(open('config.conf', 'r').read())
logging.info('configuration: ' + config['name_version'])

logging.info('Step 1: mongo db connection')
logging.info('host = {}: {}'.format(os.environ[config['mongoDB_hostConnectString']],
                              str(config['mongoDB_port'])))
client = MongoClient(os.environ[config['mongoDB_hostConnectString']],
                                config['mongoDB_port'])
db = client.news

logging.info('Step 2: fetch the rss url database')

rss_url_file = open(config['rss_url_db'], 'rb')
rss_urls = {}
cnt = 0
for line in rss_url_file:
    items = line.rstrip().split(',')
    rss_urls[items[0]] = items[1]
    cnt += 1
logging.info('found {} rss urls.'.format(cnt+1))

# -------------- Main loop ------------------------------------
logging.info('Getting to work now: running main loop')
time.sleep(1)
n = 0
out_q = Queue()   # multiprocessing queue
procs = []   # list of processes
alreadyHave = {}
while True:
    for url in rss_urls.values():
        p = Process(target=rss_worker, args=(url, out_q))
        procs.append(p)
        p.start()

    # after starting all the workers goto sleep for a short while
    time.sleep(10)

    nitems = out_q.qsize()
    for p in range(nitems):
        js = out_q.get()
        if js['title'] in alreadyHave:
            a = alreadyHave[js['title']]
        else:
            db.news.insert_one(js)
            alreadyHave[js['title']] = js
            print js['title'].encode('UTF-8', 'replace')


    for p in procs:
        p.join()

    time.sleep(2)   # sleep 5 more seconds and repeat
    """
    item_doc = { 'name': st, 'description': 'awake' + str(n) }
    for k, v in item_doc.items():
        print k, v

    db.news.insert_one(item_doc)
    """
